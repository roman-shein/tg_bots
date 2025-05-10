import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

# from config import BOT_TOKEN  # импортируем токен

dp = Dispatcher()
logger = logging.getLogger(__name__)


class Form(StatesGroup):
    entry = State()
    first = State()
    second = State()
    third = State()
    fourth = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.entry)
    await message.answer("Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Сейчас Вы находитесь в гардеробе\n"
                         "Чтобы перейти в зал №1, напишите '1'\n"
                         "В этом зале находится выставка вещей египетского вельможи\n"
                         "Чтобы выйти из музея напишите 'выход'")


@dp.message(Form.entry)
async def entry(message: Message, state: FSMContext):
    text = message.text
    if text == "1":
        await state.set_state(Form.first)
        await message.answer("В данном зале представлены следующие экспонаты:\n"
                             "1. Египетский вельможа\n"
                             "2. Обустройство его дома\n"
                             "3. Стенд с экспонатами")
        await message.answer("Чтобы перейти к выходу, напишите 'выход'\n"
                             "Чтобы перейти к залу 2, напишите '2'\n"
                             "В данном зале будут предсталены экспонаты античной эпохи")
    elif text == "выход":
        await state.clear()
        await message.answer("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    else:
        await message.answer("Я вас не понимаю :(\n"
                             "Повторите ввод")


@dp.message(Form.first)
async def first(message: Message, state: FSMContext):
    text = message.text
    if text == "выход":
        await state.clear()
        await message.answer("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!")
    elif text == "2":
        await state.set_state(Form.second)
        await message.answer("В данном зале представлены следующие экспонаты:\n"
                             "1. Древнегреческие скульптуры\n"
                             "2. Выкладки Пифагора\n"
                             "3. Бюст Евклида")
        await message.answer("Чтобы перейти к залу 3, напишите '3'\n"
                             "В данном зале будут представлены средневековые экспонаты")
    else:
        await message.answer("Я вас не понимаю :(\n"
                             "Повторите ввод")


@dp.message(Form.second)
async def second(message: Message, state: FSMContext):
    text = message.text
    if text == "3":
        await state.set_state(Form.third)
        await message.answer("В данном зале представлены следующие экспонаты:\n"
                             "1. Чумная маска\n"
                             "2. Шлемы рыцарей\n"
                             "3. Карта кретовых походов")
        await message.answer("Чтобы перейти к залу 1, напишите '1'\n"
                             "В этом зале находится выставка вещей египетского вельможи\n"
                             "Чтобы перейти к залу 4, напишите '4'\n"
                             "В этом зале будут представлены экспонаты об императорской семье в Царской России")
    else:
        await message.answer("Я вас не понимаю :(\n"
                             "Повторите ввод")


@dp.message(Form.third)
async def third(message: Message, state: FSMContext):
    text = message.text
    if text == '1':
        await state.set_state(Form.first)
        await entry(message, state)
    elif text == '4':
        await state.set_state(Form.fourth)
        await message.answer("В данном зале представлены следующие экспонаты:\n"
                             "1. Портреты членов царской семьи\n"
                             "2. Стенд имени Петра Великого\n"
                             "3. Стенд имени Екатерины Великой")
        await message.answer("Чтобы перейти к залу 1, напишите '1'\n"
                             "В этом зале находится выставка вещей египетского вельможи\n")
    else:
        await message.answer("Я вас не понимаю :(\n"
                             "Повторите ввод")


@dp.message(Form.fourth)
async def fourth(message: Message, state: FSMContext):
    text = message.text
    if text == "1":
        await state.set_state(Form.first)
        await entry(message, state)
    else:
        await message.answer("Я вас не понимаю :(\n"
                             "Повторите ввод")


BOT_TOKEN = ""


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
