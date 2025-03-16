from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog import DialogManager

from states import MainDialog
from logik import max_call_success, min_call_success, call_getter, add_food_success, get_user_foods_getter, select_food, call_adder

start_window = Window(
    Const('''Привет, я бот для подсчета калорий и бжу.
    \nТы можешь в меня добавлять еду, смотреть колько ты съел за 1 день, неделю, месяц
    \nЕще ты можешь добавлять для себя дневной лимит,
    \nбот не даст тебе съесть больше или меньше положеного
    \nНажми /menu чтобы увидеть мой потенциал'''),

    Button(Const("В меню"), id="menu",
           on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),

    state=MainDialog.start
)

menu_window = Window(
    Const("Выберите опцию:"),
    Button(Const("Задать лимит калорий"), id="call_limit",
           on_click=lambda c, b, d: d.switch_to(MainDialog.edit_call_limit)),
    Button(Const("Добавить еду"), id="add_food",
           on_click=lambda c, b, d: d.switch_to(MainDialog.add_food)),
    Button(Const("Поесть"), id="eat",
           on_click=lambda c, b, d: d.switch_to(MainDialog.food_selection)),
    state=MainDialog.menu
)

call_limit_window = Window(
    Const("Изменить лимит:\n"),

    Format("Ваш макс. лимит: {max_call}", when=F["max_call"]),
    Format("Вы не выбрали макс. лимит", when=~F["max_call"]),
    Format("Ваш мин. лимит: {min_call}", when=F["min_call"]),
    Format("Вы не выбрали мин. лимит", when=~F["min_call"]),

    Button(Const("Задать максимальный лимит"), id="max_call",
           on_click=lambda c, b, d: d.switch_to(MainDialog.add_max_call)),
    Button(Const("Задать минимальный лимит"), id="min_call",
           on_click=lambda c, b, d: d.switch_to(MainDialog.add_min_call)),
    Button(Const("🔙 Назад"), id="back",
           on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),

    state=MainDialog.edit_call_limit,
    getter=call_getter
)

add_max_call_window = Window(
    Const("Задайте ваш макс. лимит калорий:\n"),

    Format("Ваш макс. лимит: {max_call}", when=F["max_call"]),
    Format("Вы не выбрали макс. лимит", when=~F["max_call"]),
    TextInput(
        id='max_call_input',
        on_success=max_call_success,
    ),
    Button(Const("🔙 Назад"), id="back",
           on_click=lambda c, b, d: d.switch_to(MainDialog.edit_call_limit)),

    state=MainDialog.add_max_call,
    getter=call_getter
)

add_min_call_window = Window(
    Const("Задайте ваш мин. лимит калорий:\n"),

    Format("Ваш мин. лимит: {min_call}", when=F["min_call"]),
    Format("Вы не выбрали мин. лимит", when=~F["min_call"]),

    TextInput(
        id='min_call_input',
        on_success=min_call_success,
    ),
    Button(Const("🔙 Назад"), id="back",
           on_click=lambda c, b, d: d.switch_to(MainDialog.edit_call_limit)),

    state=MainDialog.add_min_call,
    getter=call_getter
)

add_food_window = Window(
    Const("Введите название и кбжу вашей еды на 100 грамм:"),
    Const("Пример: 'пельмени 250 12 8 32'"),
    TextInput(
        id='add_food_input',
        on_success=add_food_success,
    ),
    Button(Const("🔙 Назад"), id="back",
           on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),
    state=MainDialog.add_food
)

food_selection_window = Window(
    Const("Выберите еду:"),
    Const('У вас еще нет еды', when="no_food"),

    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='food',
            item_id_getter=lambda x: x[1],
            items='food',
            on_click=select_food,
        ),
        id='food_selection',
        width=1,
        height=4,
    ),

    Button(Const("🔙 Назад"), id="back", on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),

    state=MainDialog.food_selection,
    getter=get_user_foods_getter
)

grams_write_window = Window(
    Const('Введите сколько грамм вы съели:'),
    Format('Вы сегодня наели на {day_call} калорий'),
    TextInput(
        id='grams_input',
        on_success=call_adder,
    ),
    Button(Const("🔙 Назад"), id="back",
           on_click=lambda c, b, d: d.switch_to(MainDialog.food_selection)),

    state=MainDialog.write_grams,
    getter=call_getter
)

main_dialog = Dialog(
    start_window,
    menu_window,
    call_limit_window,
    add_max_call_window,
    add_min_call_window,
    add_food_window,
    food_selection_window,
    grams_write_window,
)
