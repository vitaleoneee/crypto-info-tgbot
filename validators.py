from aiogram import types


def timeout_validator(timeout):
    if int(timeout) < 1 or int(timeout) > 24:
        raise TypeError
    return timeout


def timeout_validator_filter(message: types.Message):
    try:
        timeout = timeout_validator(message.text)
    except (ValueError, TypeError):
        return None
    return {"timeout": timeout}


def direction_validator(direction):
    if direction.upper() not in ['LONG', 'SHORT']:
        raise ValueError
    return direction


def direction_validator_filter(message: types.Message):
    try:
        direction = direction_validator(message.text)
    except (ValueError, TypeError):
        return None
    return {"direction": direction}


def price_validator(price):
    try:
        return float(price)
    except (ValueError, TypeError):
        raise ValueError("Not a valid float")


def price_validator_filter(message: types.Message):
    try:
        price = price_validator(message.text)
    except (ValueError, TypeError):
        return None
    return {"price": price}
