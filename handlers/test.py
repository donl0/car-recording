from aiogram import Bot, Dispatcher
from aiogram import types

from settings.client_connect import client


async def backs_handlers(bot: Bot, dp: Dispatcher):
    @dp.message_handler(text='a')
    async def comm_back(message: types.Message):
        id_person = message.chat.id
        await bot.send_message(chat_id=id_person, text='da')
        sheet = client.open('table1')
        sheet = sheet.worksheet('car info')

        all_products = sheet.col_values(1)
