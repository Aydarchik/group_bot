from aiogram.fsm.state import State, StatesGroup

class MainDialog(StatesGroup):
    start = State()
    menu = State()
