from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database import db_manager
from states import MainDialog


async def call_success(message: Message, widget: ManagedTextInput,
                          dialog_manager: DialogManager, call: int, limit: str):
    tg_id = message.from_user.id

    try:
        int_call = int(call)

    except ValueError:
        await message.answer("Введите целое число")
        return

    if limit == 'max':
        db_manager.add_max_call(
            tg_id=tg_id,
            max_call=int_call,
        )
        await dialog_manager.switch_to(MainDialog.add_max_call)

    elif limit == 'min':
        db_manager.add_min_call(
            tg_id=tg_id,
            min_call=int_call,
        )
        await dialog_manager.switch_to(MainDialog.add_min_call)

    await message.delete()

async def max_call_success(message: Message, widget: ManagedTextInput,
                          dialog_manager: DialogManager, call: int):
    await call_success(
        message=message,
        widget=widget,
        dialog_manager=dialog_manager,
        call=call,
        limit='max',
    )

async def min_call_success(message: Message, widget: ManagedTextInput,
                          dialog_manager: DialogManager, call: int):
    await call_success(
        message=message,
        widget=widget,
        dialog_manager=dialog_manager,
        call=call,
        limit='min',
    )


async def call_getter(dialog_manager: DialogManager, **_):
    tg_id = dialog_manager.dialog_data.get('tg_id', None)

    user = db_manager.select_user(tg_id=tg_id)

    print(tg_id, user)

    return {
        'max_call': user['max_call'],
        'min_call': user['min_call'],
        'day_call': user['day_call'],
    }

async def add_food_success(message: Message, widget: ManagedTextInput,
                          dialog_manager: DialogManager, food: str):
    data = food.split()

    if len(data) != 5:
        await message.answer("Необходимо ввести 5 значений через пробел (название, калории, белки, жиры, углеводы).")
        return

    try:
        food, *calls = data
        calls = [int(call) for call in calls]

        if any(call < 0 for call in calls):
            await message.answer("Значения калорий, белков, жиров и углеводов не могут быть отрицательными.")
            return

        db_manager.add_food(
            tg_id=message.from_user.id,
            food=data[0],
            food_call=data[1],
            protein=data[2],
            fat=data[3],
            carbohydrates=data[4],
        )
        await message.answer(
            f"Добавлено: {food}, {calls[0]} ккал, {calls[1]} Б, {calls[2]} Ж, {calls[3]} У."
        )
    except ValueError:
        await message.answer("Калории, белки, жиры и углеводы должны быть числами.")
        return

    await message.delete()
    await dialog_manager.switch_to(MainDialog.add_food)




async def get_user_foods_getter(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    foods = db_manager.select_user_food(tg_id=user_id)
    dialog_manager.dialog_data["foods"] = foods

    if foods:
        buttons = [(
                f"{food['name']}", food['id']) for food in foods]

        return {"food": buttons, "no_food": False}

    return {"food": [], "no_food": True}

async def select_food(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                    item_id: str):
    foods = dialog_manager.dialog_data.get("foods", [])

    selected_food = next((food for food in foods if food['id'] == int(item_id)), None)


    print(selected_food)
    if not selected_food:
        await callback.answer("Еда не найдена!")
        return

    dialog_manager.dialog_data["food_id"] = selected_food['id']
    dialog_manager.dialog_data["food_call"] = selected_food['food_call']

    await dialog_manager.switch_to(state=MainDialog.write_grams)


async def call_adder(message: Message, widget: ManagedTextInput,
                          dialog_manager: DialogManager, grams: str):
    try:
        int_grams = int(grams) / 100
    except ValueError:
        await message.answer("Введите целое число")
        return

    food_call = dialog_manager.dialog_data.get('food_call', None)

    day_call = db_manager.select_user_day_call(tg_id=message.from_user.id)
    print(day_call)
    print(day_call[0])
    float_call = (int_grams * food_call) // 1
    current_day_call = day_call[0] + int(float_call)
    db_manager.add_day_call(
        tg_id=message.from_user.id,
        day_call=current_day_call,
    )
    await message.delete()
    await dialog_manager.switch_to(MainDialog.write_grams)





