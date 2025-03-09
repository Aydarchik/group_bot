from aiogram.fsm.state import State, StatesGroup

class MainDialog(StatesGroup):
    start = State()
    menu = State()
    edit_call_limit = State()
