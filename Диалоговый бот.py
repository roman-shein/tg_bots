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


class Form(StatesGroup):  # создаем статусы, через которые будет проходить пользователь
    weather = State()
    locality = State()


@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Form.locality)  # установливаем статус locality
    await message.answer(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?", reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Command("skip"))
async def skip(message: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == Form.locality:
        await state.set_state(Form.weather)
        await message.answer("Какая погода у вас за окном?")
    else:
        await message.answer("Вы не можете пропустить этот вопрос")


@dp.message(Command("stop"))
@dp.message(F.text.casefold() == "stop")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # получаем текущий статус
    if current_state is None:  # если статус не установлен, то ничего не делаем
        return

    logging.info("Отмена на шаге %r", current_state)
    await state.clear()  # статусы очищены
    await message.answer(
        "Всего доброго!",
    )


@dp.message(Form.locality)  # обработчик для определенного статуса
async def process_locality(message: Message, state: FSMContext):
    await state.set_state(Form.weather)  # установлен статус weather
    locality = message.text
    await message.answer(
        f"Какая погода в городе {locality}?")


@dp.message(Form.weather)  # обработчик для определенного статуса
async def process_weather(message: Message, state: FSMContext):
    await state.clear()  # статусы очищены
    weather = message.text
    logger.info(f"погода {weather}")
    await message.answer(
        "Спасибо за участие в опросе! Всего доброго!")


BOT_TOKEN = ""


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # Запускаем логгирование
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())  # начинаем принимать сообщения
