from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

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

main_dialog = Dialog(
    start_window,
)