import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import json
from random import choice
import os

# from config import BOT_TOKEN  # импортируем токен

dp = Dispatcher()
logger = logging.getLogger(__name__)

BOT_TOKEN = ""
bot = Bot(token=BOT_TOKEN)

users = {}
questions = {}


async def main():
    await dp.start_polling(bot)


class Form(StatesGroup):
    wait_file = State()
    testing = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.wait_file)
    await message.answer("Загрузите файл с вопросами в формате json", reply_markup=ReplyKeyboardRemove())


@dp.message(Command("stop"))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        user_id = message.from_user.id
        await state.clear()
        await message.answer("Уже уходите? Возвращайтесь!")
        del users[user_id]
        del questions[user_id]
        os.remove(fr"data\{user_id}.json")
    else:
        return


@dp.message(Form.wait_file)
async def get_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        await Bot.download(bot, message.document.file_id, fr"data\{user_id}.json", 120)
        with open(fr"data\{user_id}.json", 'r', encoding="utf8") as fin:
            data = json.load(fin)
            users[user_id] = data["test"]
        await state.set_state(Form.testing)
        questions[user_id] = choice(users[user_id])
        await message.answer("Для того чтобы начать тестирование, напишите 'поехали!'")
    except AttributeError:
        await message.answer("Вы не загрузили файл\n"
                             "Повторите попытку")


@dp.message(Form.testing)
async def testing(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    if text != "поехали!":
        if text == questions[user_id]["response"]:
            await message.answer("Правильно!")
        else:
            await message.answer(f"Неверное. Правильный ответ: {questions[user_id]['response']}")
        users[user_id].remove(questions[user_id])
        if users[user_id]:
            questions[user_id] = choice(users[user_id])
            await message.answer(f"Следующий вопрос: {questions[user_id]['question']}")
        else:
            await message.answer("Вопросов больше нет!")
            await state.clear()
            del questions[user_id]
            del users[user_id]
            await message.answer("Чтобы повторить, введите /start")
    else:
        await message.answer(f"{questions[user_id]['question']}")


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
