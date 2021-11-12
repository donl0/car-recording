
from aiogram import Bot, Dispatcher
from aiogram import types
from settings.config import chat_to_send_id
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times
from utils.logic import rewrite_rec
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def buttons_callback_handler(bot: Bot, dp: Dispatcher):

    @dp.callback_query_handler(rewrite_rec.filter(action_name='rewrite'))
    async def rewrite_brand(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
        #print(query)
        date_cell = callback_data['date']
        time_cell = callback_data['time']
        brand = callback_data['brand']
        sheet = get_sheet("TO", "car info")
        text = query.message['text']
        text = text.split('/n')
        await state.update_data(query=query, sheet=sheet, callback_data=callback_data)
        #text[2]=
        #model_change_wait
        await OrderDataUser.model_change_wait.set()
        #print(text)
        #text = query['reply_to_message'].text
      #  print(text)
        await bot.send_message(query.from_user['id'], 'Введите новую модель машины')
        #sheet.update_cell(time_cell, date_cell, brand)
        #await bot.edit_message_reply_markup(chat_id=id_person, message_id=call.message.message_id,
          #                                  reply_markup=film_info[7])

    @dp.message_handler(state=OrderDataUser.model_change_wait)
    async def last(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        new_model = message.text
        user_data = await state.get_data()
        print(user_data)
        #group_data
        text = user_data['query'].message['text']
        text = text.split('\n')
        text[2] = new_model
        str=''
        for i in text:
            str += i+'\n'

        action_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
        item_change = InlineKeyboardButton('Изменить', callback_data=rewrite_rec.new(action_name='rewrite',
                                                                                     date=user_data['callback_data'][
                                                                                         'date'],
                                                                                     time=user_data['callback_data'][
                                                                                         'time'],
                                                                                     brand=new_model,
                                                                                     group_data=user_data['callback_data']['group_data']))
        action_keyboard.add(item_change)
        await bot.edit_message_text(chat_id=chat_to_send_id,
                                    text=str,
                                    message_id=user_data['callback_data']['group_data'])
        await bot.edit_message_text(chat_id=id_person,
                                    message_id=user_data['query'].message.message_id,
                                    text=str,
                                    reply_markup=action_keyboard)