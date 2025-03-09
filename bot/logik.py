from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
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

