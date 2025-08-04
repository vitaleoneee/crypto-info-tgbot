from aiogram.fsm.state import StatesGroup, State


class PriceState(StatesGroup):
    cryptocurrency = State()


class AlertState(StatesGroup):
    cryptocurrency_alert = State()
    timeout = State()
    direction = State()
    price = State()
