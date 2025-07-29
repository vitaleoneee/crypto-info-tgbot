import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from decouple import config

from get_crypto_data import get_crypto_info

BOT_TOKEN = config('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(text='Программа запущенна')


@dp.message()
async def crypto_response(message: types.Message):
    crypto_info = get_crypto_info(message.text)
    await message.answer(text=str(crypto_info))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
