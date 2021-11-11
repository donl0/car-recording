from aiogram import Bot, Dispatcher
from aiogram import types
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times
from utils.logic import rewrite_rec

async def back_handler(bot: Bot, dp: Dispatcher):

    @dp.callback_query_handler(rewrite_rec.filter(action='rewrite'))
    async def rewrite_record(query: types.CallbackQuery, callback_data: dict):
        rewrite_data = [callback_data['day'], callback_data['time']]
        print(rewrite_data)