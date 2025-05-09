import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
# from config import BOT_TOKEN
import logging
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()

BOT_TOKEN = ""


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


@dp.message(Command("start"))
async def start(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Привет {name}! Я эхо-бот. Напиши мне что-нибудь, и я пришлю это назад!")


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Я пока не умею помогать... Я только ваше эхо.")


@dp.message(Command("time"))
async def get_time(message: types.Message):
    t = datetime.now().time().strftime("%H:%M:%S")
    await message.answer(f"{t}")


@dp.message(Command("date"))
async def get_date(message: types.Message):
    d = datetime.now().date().strftime("%d-%B-%Y")
    await message.answer(f"{d}")


@dp.message()
async def answer_to_message(message: types.Message):
    await message.answer(f"Я получил сообщение <{message.text}>")


if __name__ == "__main__":
    asyncio.run(main())
