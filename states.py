from aiogram.fsm.state import StatesGroup, State


class PriceState(StatesGroup):
    cryptocurrency = State()
