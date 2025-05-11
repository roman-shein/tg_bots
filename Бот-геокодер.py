import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import requests

from config import BOT_TOKEN  # импортируем токен

dp = Dispatcher()
logger = logging.getLogger(__name__)

# BOT_TOKEN = ""
bot = Bot(token=BOT_TOKEN)


async def main():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот-геокодер, введите название объекта и я покажу его на карте",
                         reply_markup=ReplyKeyboardRemove())


@dp.message()
async def get_ll(message: Message):
    geocoder_url = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_api_key = "cf79098a-155e-47b7-9b49-b55b4461472d"
    geocoder_params = {
        "apikey": geocoder_api_key,
        "geocode": message.text,
        "format": "json"
    }
    response = await get_response(geocoder_url, params=geocoder_params)
    response = response["response"]["GeoObjectCollection"]["featureMember"]
    if not response:
        await message.answer("По вашему запросу ничего не найдено :(")
        return
    ll = ','.join(response[0]["GeoObject"]["Point"]["pos"].split() + ["pm2gnl"])

    lower_corner = response[0]["GeoObject"]['boundedBy']['Envelope']['lowerCorner']
    upper_corner = response[0]["GeoObject"]['boundedBy']['Envelope']['upperCorner']

    lon1, lat1 = map(float, lower_corner.split())
    lon2, lat2 = map(float, upper_corner.split())

    spn = str(abs(lon1 - lon2)), str(abs(lat1 - lat2))
    spn = ",".join(spn)

    static_api_server = "https://static-maps.yandex.ru/v1?"
    static_api_key = "318965a9-b51c-41fb-a672-2acad73bc050"
    static_api_params = {
        "apikey": static_api_key,
        "spn": spn,
        "pt": ll
    }
    # url = requests.get(static_api_server, params=static_api_params).url
    url = f"{static_api_server}spn={static_api_params['spn']}&pt={ll}&apikey={static_api_key}"
    await message.answer_photo(url, caption="Нашел")


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url, params=params) as resp:
            return await resp.json()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
    )
    asyncio.run(main())
