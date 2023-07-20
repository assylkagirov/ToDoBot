from dotenv import load_dotenv
load_dotenv()

import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_hello(message: types.Message):
    await message.reply("Hello, world!")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Unknown command. Type /start to see the Hello, world! message.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
