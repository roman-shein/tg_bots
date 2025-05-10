import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from translate import Translator

# from config import BOT_TOKEN  # импортируем токен

dp = Dispatcher()
logger = logging.getLogger(__name__)

BOT_TOKEN = ""
bot = Bot(token=BOT_TOKEN)

users = {}


class Form(StatesGroup):
    from_rus_to_eng = State()
    from_eng_to_rus = State()


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.from_rus_to_eng)
    users[message.from_user.id] = "ru"
    await message.answer("Текущее направление перевода с русского на английский", reply_markup=ReplyKeyboardRemove())
    await message.answer("Введите текст", reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/eng")]], resize_keyboard=True, one_time_keyboard=False
    ))


@dp.message(Command("eng"))
@dp.message(Command("ru"))
async def change(message: Message, state: FSMContext):
    text = message.text
    if text == "/eng" and await state.get_state() == Form.from_rus_to_eng:
        await state.set_state(Form.from_eng_to_rus)
        await message.answer("Текущее направление перевода с английского на русский",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer("Enter the text", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/ru")]], resize_keyboard=True, one_time_keyboard=False
        ))
    elif text == "/ru" and await state.get_state() == Form.from_eng_to_rus:
        await state.set_state(Form.from_rus_to_eng)
        await message.answer("Текущее направление перевода с русского на английский",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer("Введите текст", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="/eng")]], resize_keyboard=True, one_time_keyboard=False
        ))


@dp.message(Form.from_rus_to_eng)
@dp.message(Form.from_eng_to_rus)
async def translate(message: Message, state: FSMContext):
    try:
        cur_state = await state.get_state()
        text = message.text
        if cur_state == Form.from_rus_to_eng:
            translator = Translator(from_lang="russian", to_lang="english")
            new_text = translator.translate(text)
            await message.answer(new_text)
        elif cur_state == Form.from_eng_to_rus:
            translator = Translator(from_lang="english", to_lang="russian")
            new_text = translator.translate(text)
            await message.answer(new_text)
    except Exception:
        await message.answer("Ошибка перевода!")


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
