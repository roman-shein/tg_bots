import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN
import logging
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

dp = Dispatcher()

# BOT_TOKEN = ""
arr = {}


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


class Tasks:
    def __init__(self, t):
        self.t = t

    async def start_task(self):
        await asyncio.sleep(self.t)


@dp.message(Command("set"))
async def set_timer(message: types.Message):
    try:
        people_id = message.from_user.id
        timer = int(message.text.split()[1])
        task = Tasks(timer)
        t = datetime.now()
        if people_id in arr and arr[people_id]:
            await message.answer("Предыдущая задача удалена")
            arr[people_id] = []
        arr[people_id] = [t]
        await task.start_task()
        if t in arr[people_id]:
            await message.answer(f"{timer} секунд прошли!")
            arr[people_id] = []
    except ValueError:
        await message.answer("Вы передали не число")
    except IndexError:
        await message.answer("Вы передали пустой параметр")


@dp.message(Command("unset"))
async def unset_timer(message: types.Message):
    people_id = message.from_user.id
    if arr[people_id]:
        arr[people_id] = []
        await message.answer("Текущая задача удалена")
    else:
        await message.answer("У вас нет текущих задач")


if __name__ == "__main__":
    asyncio.run(main())
