import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from decouple import config

from get_crypto_data import get_assets_price

BOT_TOKEN = config('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        text='Hello!\nThis bot was created to display up-to-date information about cryptocurrency.\n\n'
             'Type /help to find out what it can do.')


@dp.message(Command('price'))
async def crypto_response(message: types.Message):
    args = message.text.split()
    if len(args) > 2:
        await message.answer(text='❌ You used the /price command incorrectly, reread /help and try again.')
    # If the command was called without additional arguments
    elif len(args) == 1:
        send_text = '<b>🔥 Popular crypto derivatives right now (Futures)</b>:\n\n'
        crypto_info = get_assets_price()
        send_text += crypto_info
        await message.answer(text=str(send_text), parse_mode='HTML')
    else:
        send_text = f'<b>🔥 Info about your coin(s) - {args[1].upper()}</b>:\n\n'
        crypto_info = get_assets_price(args[1])
        send_text += crypto_info
        await message.answer(text=str(send_text), parse_mode='HTML')


@dp.message(Command('help'))
async def help_response(message: types.Message):
    await message.answer(text='Type /price to get prices of the most popular assets.\n'
                              'Add the name of the cryptocurrency to the command to get details about it (e.g. "ВТС" or "btc")'
                              ' or add several names separated by commas (e.g. "ВТС, ЕТН, ada" or "btc, LINK, avax")'
                              ' to get information about several cryptocurrencies at once.\nEnjoy!')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
