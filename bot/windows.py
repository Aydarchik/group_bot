from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput

from states import MainDialog
from logik import max_call_success, min_call_success, call_getter

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
           on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),
    Button(Const("Поесть"), id="eat",
           on_click=lambda c, b, d: d.switch_to(MainDialog.menu)),
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

main_dialog = Dialog(
    start_window,
    menu_window,
    call_limit_window,
    add_max_call_window,
    add_min_call_window,
)
