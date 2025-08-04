import asyncio
import logging

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from decouple import config

from constants import MAX_TOP_SIZE, HELP_TEXT
from get_crypto_data import get_assets_price, get_top_capitalization
from states import PriceState, AlertState
from validators import timeout_validator_filter, price_validator_filter, direction_validator_filter
from utils import parse_command_args, create_alert_task

BOT_TOKEN = config('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def response_text(message: types.Message, text: str):
    await message.answer(text=text, parse_mode='HTML')


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        text='Hello!\nThis bot was created to display up-to-date information about cryptocurrency.\n\n'
             'Type /help to find out what it can do.')


@dp.message(Command('price'))
async def handle_price_start(message: types.Message, state: FSMContext):
    await state.set_state(PriceState.cryptocurrency)
    await response_text(message, 'Enter the name of the cryptocurrency(ies) 🪙:')


@dp.message(PriceState.cryptocurrency, F.text)
async def handle_cryptocurrency_price(message: types.Message, state: FSMContext):
    await state.update_data(cryptocurrency=message.text)
    await state.clear()
    crypto_info = get_assets_price(message.text)
    await response_text(message, str(crypto_info))


@dp.message(PriceState.cryptocurrency)
async def handle_cryptocurrency_price_invalid(message: types.Message):
    await response_text(message, '❌ You entered something that is not text. Try again.')


@dp.message(Command('alert'))
async def handle_alert_start(message: types.Message, state: FSMContext):
    await state.set_state(AlertState.cryptocurrency_alert)
    await response_text(message, 'Enter the name of the cryptocurrency you want to set an alert for ⏰:')


@dp.message(AlertState.cryptocurrency_alert, F.text)
async def handle_alert_cryptocurrency(message: types.Message, state: FSMContext):
    await state.update_data(cryptocurrency_alert=message.text)
    await state.set_state(AlertState.timeout)
    await response_text(message, 'Enter the timeout in hours:')


@dp.message(AlertState.cryptocurrency_alert)
async def handle_alert_cryptocurrency_invalid(message: types.Message):
    await response_text(message, '❌ You entered something that is not text. Try again.')


@dp.message(AlertState.timeout, timeout_validator_filter)
async def handle_alert_timeout(message: types.Message, state: FSMContext, timeout: str):
    await state.update_data(timeout=timeout)
    await state.set_state(AlertState.direction)
    await response_text(message, 'Enter the direction (LONG or SHORT):')


@dp.message(AlertState.timeout)
async def handle_alert_timeout_invalid(message: types.Message):
    await response_text(message,
                        '❌ You entered something that is not text or your value is incorrect (max 24 hours). Try again.')


@dp.message(AlertState.direction, direction_validator_filter)
async def handle_alert_direction(message: types.Message, state: FSMContext, direction: str):
    await state.update_data(direction=direction)
    await state.set_state(AlertState.price)
    await response_text(message, 'Enter the cryptocurrency price at which the alert will be triggered 💲:')


@dp.message(AlertState.direction)
async def handle_alert_direction_invalid(message: types.Message):
    await response_text(message,
                        '❌ You entered something that is not text or your value is incorrect. Try again.')


@dp.message(AlertState.price, price_validator_filter)
async def handle_alert_price(message: types.Message, state: FSMContext, price: str):
    await state.update_data(price=price)
    data = await state.get_data()
    await state.clear()
    await response_text(message,
                        f"⏳ Alert for {data['cryptocurrency_alert'].upper()} started. Monitoring for {data['timeout']} hour(s)...")
    asyncio.create_task(
        create_alert_task(bot, message.chat.id, data['cryptocurrency_alert'], data['timeout'], data['price'],
                          data['direction']))


@dp.message(AlertState.price)
async def handle_alert_price_invalid(message: types.Message):
    await response_text(message, '❌ You entered something that is not a valid price format. Try again.')


@dp.message(Command('top'))
async def top_response(message: types.Message):
    status, args = parse_command_args(message)
    if status == 'too_many':
        await response_text(message, text='❌ You used the /top command incorrectly, reread /help and try again.')
        return
    elif status == 'none':
        top_assets = get_top_capitalization()
        await response_text(message, str(top_assets))
    else:
        try:
            if int(args[0]) > MAX_TOP_SIZE or int(args[0]) < 0:
                await response_text(message, '❌ The maximum number of assets in the top is 50!')
                return
        except ValueError:
            await response_text(message, '❌ You entered something other than a number!')
            return
        top_assets = get_top_capitalization(args[0])
        await response_text(message, top_assets)


@dp.message(Command('help'))
async def help_response(message: types.Message):
    await response_text(message, HELP_TEXT)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
