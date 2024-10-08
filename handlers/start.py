from aiogram import Bot, Dispatcher
from aiogram import types
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from settings.config import chat_to_send_id
from utils.get_day import get_day_num_cell, get_all_days, normalize
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times


async def start_handler(bot: Bot, dp: Dispatcher):
    @dp.message_handler(commands=['start'], state="*")
    async def start(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        if message['chat']['type'] == 'private':
            #x = await bot.send_message(chat_id = chat_to_send_id, text='aa')
           # print(x.message_id)
            await bot.send_message(chat_id=id_person, text='https://docs.google.com/spreadsheets/d/1C5YqE3QYlte15z6OsKF_cSVs-A9HxAkDIRs9oPQG--w/edit?usp=sharing', reply_markup=to_keyboard)
           # await bot.edit_message_text(chat_id=chat_to_send_id,
           #                             text='ASAXXAXA',
           #                             message_id=x.message_id)
            await state.finish()
