from aiogram.fsm.state import State, StatesGroup

class MainDialog(StatesGroup):
    start = State()
    menu = State()
    edit_call_limit = State()
    add_min_call = State()
    add_max_call = State()
    add_food = State()
    food_selection = State()
    write_grams = State()
