import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
# from config import BOT_TOKEN
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()


BOT_TOKEN = ""
async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


@dp.message()
async def answer_to_message(message: types.Message):
    await message.answer(f"Я получил сообщение <{message.text}>")


if __name__ == "__main__":
    asyncio.run(main())
