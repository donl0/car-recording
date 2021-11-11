import asyncio
from aiogram import Bot, Dispatcher

from midlware.big_brother import BigBrother
from handlers.sheet_pull import to_handler
from handlers.clear_cell import clear_cell_handler
from handlers.start import start_handler
from handlers.back import back_handler
from handlers.last_handler import last_handler
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings.config import TG_TOKEN


async def bot_settings(loop=None):
    bot = Bot(token=TG_TOKEN, parse_mode='HTML', loop=loop)
    dp = Dispatcher(bot, storage=MemoryStorage())

    await start_handler(bot, dp)
    await to_handler(bot, dp)
    await clear_cell_handler(bot, dp)
    await back_handler(bot, dp)
    await last_handler(bot, dp)

    return bot, dp


async def polling():
    bot, dp = await bot_settings()
    dp.middleware.setup(BigBrother())
    try:
        await dp.start_polling()
    finally:
        await bot.close()


def handle():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        asyncio.run(polling())


handle()


def dp():
    return None