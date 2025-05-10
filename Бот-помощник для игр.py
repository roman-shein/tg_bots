import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
# from config import BOT_TOKEN
import logging
from random import randint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()

BOT_TOKEN = ""

tasks = {}


class Timer:
    def __init__(self, t):
        self.t = t

    async def start_timer(self):
        await asyncio.sleep(self.t)


@dp.message(Command("start"))
async def start(message: types.Message, new_player=True):
    btns = [[KeyboardButton(text="/dice"), KeyboardButton(text="/timer")]]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True, one_time_keyboard=False)
    if new_player:
        await message.answer("Привет!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Вы венулись в стартовое меню", reply_markup=ReplyKeyboardRemove())
    await message.answer("Теперь вы можете выбрать режим", reply_markup=kb)


@dp.message(Command("dice"))
async def dice(message: types.Message):
    btns = [[KeyboardButton(text="Кинуть один шестигранный кубик")],
            [KeyboardButton(text="Кинуть два шестигранных кубика")],
            [KeyboardButton(text="Кинуть 20-гранный кубик")],
            [KeyboardButton(text="Вернуться назад")]]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True, one_time_keyboard=False)
    await message.answer("Вы перешли в режим броска кубика", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберете, что хотите бросить", reply_markup=kb)


@dp.message(Command("timer"))
async def set_timer(message: types.Message, reverse=True):
    btns = [[KeyboardButton(text="30 секунд")],
            [KeyboardButton(text="1 минута")],
            [KeyboardButton(text="5 минут")],
            [KeyboardButton(text="Вернуться назад")]]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True, one_time_keyboard=False)
    if reverse:
        await message.answer("Вы перешли в режим таймера", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберете время", reply_markup=kb)


@dp.message(Command("close"))
async def close(message: types.Message):
    tasks[message.from_user.id] = None
    btns = [[KeyboardButton(text="30 секунд")],
            [KeyboardButton(text="1 минута")],
            [KeyboardButton(text="5 минут")],
            [KeyboardButton(text="Вернуться назад")]]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True, one_time_keyboard=False)
    await message.answer("Текущий таймер сброшен", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы вернулись в режим выбора времени", reply_markup=kb)


@dp.message()
async def answer_for_message(message: types.Message):
    text = message.text
    if text == "Вернуться назад":
        await start(message, new_player=False)
    elif text == "Кинуть один шестигранный кубик":
        await message.answer(f"{randint(1, 6)}")
    elif text == "Кинуть два шестигранных кубика":
        await message.answer(f"{randint(1, 6)} {randint(1, 6)}")
    elif text == "Кинуть 20-гранный кубик":
        await message.answer(f"{randint(1, 20)}")
    elif text == "30 секунд":
        task = Timer(30)
        tasks[message.from_user.id] = task
        await message.answer(f"засек 30 секунд", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/close")]], resize_keyboard=True, one_time_keyboard=False))
        await task.start_timer()
        if tasks[message.from_user.id] is not None:
            await message.answer("30 секунд истекло", reply_markup=ReplyKeyboardRemove())
            tasks[message.from_user.id] = None
            await set_timer(message, reverse=False)
    elif text == "1 минута":
        task = Timer(60)
        tasks[message.from_user.id] = task
        await message.answer(f"засек 1 минуту", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/close")]], resize_keyboard=True, one_time_keyboard=False))
        await task.start_timer()
        if tasks[message.from_user.id] is not None:
            await message.answer("1 минута истекла", reply_markup=ReplyKeyboardRemove())
            tasks[message.from_user.id] = None
            await set_timer(message, reverse=False)
    elif text == "5 минут":
        task = Timer(300)
        tasks[message.from_user.id] = task
        await message.answer(f"засек 5 минут", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/close")]], resize_keyboard=True, one_time_keyboard=False))
        await task.start_timer()
        if tasks[message.from_user.id] is not None:
            await message.answer("5 минут истекло", reply_markup=ReplyKeyboardRemove())
            tasks[message.from_user.id] = None
            await set_timer(message, reverse=False)


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
