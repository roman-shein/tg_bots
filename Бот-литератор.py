import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config import BOT_TOKEN  # импортируем токен

dp = Dispatcher()
logger = logging.getLogger(__name__)

text_song = [
    "Белый снег, серый лед",
    "На растрескавшейся земле",
    "Одеялом лоскутным на ней",
    "Город в дорожной петле",
    "А над городом плывут облака",
    "Закрывая небесный свет",
    "А над городом желтый дым",
    "Городу две тысячи лет",
    "Прожитых под светом звезды по имени Солнце",
    "И две тысячи лет война",
    "Война без особых причин",
    "Война дело молодых",
    "Лекарство против морщин",
    "Красная-красная кровь",
    "Через час уже просто земля",
    "Через два - на ней цветы и трава",
    "Через три - она снова жива",
    "И согрета лучами звезды по имени Солнце",
    "И мы знаем, что так было всегда",
    "Что судьбою больше любим",
    "Кто живет по законам другим",
    "И кому умирать молодым",
    "Он не помноит слова да и слова нет",
    "Он не помнит ни чинов, ни имен",
    "И способен дотянуться до звезд",
    "Не считая, что это сон",
    "И упасть опаленным звездой по имени Солнце"
]

users = {}


class Form(StatesGroup):
    work = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f"{text_song[0]}", reply_markup=ReplyKeyboardRemove())
    users[message.from_user.id] = 1
    await state.set_state(Form.work)


@dp.message(Command("stop"))
async def stop(message: Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.answer("Уже уходите? Возвращайтесь, пожалуйста!")
        del users[message.from_user.id]
    else:
        return


@dp.message(Form.work)
async def get_message(message: Message, state: FSMContext):
    text = message.text
    key = users[message.from_user.id]
    if text == text_song[key]:
        try:
            await message.answer(f"{text_song[key + 1]}")
            users[message.from_user.id] += 2
            c = text_song[users[message.from_user.id]]
        except IndexError:
            await state.clear()
            await message.answer("Ура, мы сделали это\n"
                                 "Чтобы повторить введи /start")
    else:
        await message.answer("нет, не так")
        await suphler(message, state)


@dp.message(Command("suphler"))
async def suphler(message: Message, state: FSMContext):
    await message.answer(f"{text_song[users[message.from_user.id]]}")


# BOT_TOKEN = ""


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
