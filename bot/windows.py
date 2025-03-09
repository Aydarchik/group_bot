from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from states import MainDialog


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
    Format("Ваш мин. лимит: max_call"),
    Format("Ваш макс. лимит: min_call"),
    Const("\nИзменить лимит:"),
    Button(Const("Задать максимальный лимит"), id="max_call",
           on_click=lambda c, b, d: d.switch_to(MainDialog.edit_call_limit)),
    Button(Const("Задать максимальный лимит"), id="min_call",
           on_click=lambda c, b, d: d.switch_to(MainDialog.edit_call_limit)),
    state=MainDialog.edit_call_limit
)

main_dialog = Dialog(
    start_window,
    menu_window,
    call_limit_window,
)