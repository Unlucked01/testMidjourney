from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    img_gen = State()
    img_red = State()

