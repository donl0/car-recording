
from aiogram import Bot, Dispatcher
from aiogram import types
from settings.config import chat_to_send_id
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.get_time_ccel import from_your_time_to_cell
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times
from utils.logic import rewrite_rec, rewrite_date
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def buttons_callback_handler(bot: Bot, dp: Dispatcher):

    @dp.callback_query_handler(rewrite_rec.filter(action_name='rewrite'), state="*")
    async def rewrite_brand(query: types.CallbackQuery, callback_data: dict, state: FSMContext):

     #   button1=query.message['reply_markup']['inline_keyboard'][0][0]
        await state.update_data(query=query, callback_data=callback_data)


        await bot.send_message(query.from_user['id'], 'Введите новую модель машины')

        await OrderDataUser.model_change_wait.set()
        #sheet.update_cell(time_cell, date_cell, brand)
        #await bot.edit_message_reply_markup(chat_id=id_person, message_id=call.message.message_id,
          #                                  reply_markup=film_info[7])

    @dp.message_handler(state=OrderDataUser.model_change_wait)
    async def last(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        new_model = message.text
        await state.update_data(brand=new_model)
        await bot.send_message(id_person, 'Введите пробег')
        await OrderDataUser.model_change_wait22.set()

    @dp.message_handler(state=OrderDataUser.model_change_wait22)
    async def last(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        new_distant = message.text
        user_data = await state.get_data()
        #group_data
        text = user_data['query'].message['text']
        text = text.split('\n')
        text[2] = user_data['brand']
        text[3] = new_distant
        str=''
        for i in text:
            str += i+'\n'

        action_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        item_change = InlineKeyboardButton('Изменить машину', callback_data=rewrite_rec.new(action_name='rewrite',
                                                                                     date=user_data['callback_data'][
                                                                                         'date'],
                                                                                     time=user_data['callback_data'][
                                                                                         'time'],
                                                                                     brand=user_data['brand'],
                                                                                            distant=new_distant,
                                                                                     group_data=user_data['callback_data']['group_data']))
        item_change_date = InlineKeyboardButton('Изменить дату', callback_data=rewrite_date.new(action_name='rewrite_date',
                                                                                            date=
                                                                                            user_data['callback_data'][
                                                                                                'date'],
                                                                                            time=
                                                                                            user_data['callback_data'][
                                                                                                'time'],
                                                                                               brand=user_data['brand'],
                                                                                                distant=new_distant,
                                                                                            group_data=
                                                                                            user_data['callback_data'][
                                                                                                'group_data']))
        action_keyboard.add(item_change, item_change_date)
        #await bot.edit_message_text(chat_id=chat_to_send_id,
        #                           text='ASAXXAXA',
         #                           message_id=x.message_id)

        await bot.edit_message_text(chat_id=chat_to_send_id,
                                    text=str,
                                    message_id=user_data['callback_data']['group_data'])
        await bot.edit_message_text(chat_id=id_person,
                                    message_id=user_data['query'].message.message_id,
                                    text=str,
                                    reply_markup=action_keyboard)

        sheet = get_sheet("TO", "car info")
        sheet.update_cell(user_data['callback_data']['time'], user_data['callback_data']['date'], user_data['brand'])
        await state.finish()

    @dp.callback_query_handler(rewrite_date.filter(action_name='rewrite_date'), state="*")
    async def rewrite_brand(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
        await state.update_data(query=query, callback_data=callback_data)

        await bot.send_message(query.from_user['id'], 'Выберите день', reply_markup=days_keyboard())
        await OrderDataUser.day_wait_change.set()

    @dp.message_handler(state=OrderDataUser.day_wait_change)
    async def get_day(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        day_cell = get_day_num_cell(message.text)
        await state.update_data(day=day_cell)
        await state.update_data(day_str=message.text)

        # await bot.send_message(chat_id=id_person, text='Выберите время', reply_markup=times_keyboard())
        await message.reply(text='Выберите время', reply_markup=times_keyboard(day_cell))
        await OrderDataUser.time_wait_change.set()

    @dp.message_handler(state=OrderDataUser.time_wait_change)
    async def get_time_for_sheep(message: types.Message, state: FSMContext):
        id_person = message.chat.id

        await state.update_data(time=from_your_time_to_cell(message.text))
        await state.update_data(time_str=message.text)
        # await bot.send_message(chat_id=id_person, text='Введите название машины', reply_markup=back_keyboard)

        user_data = await state.get_data()
        text = user_data['query'].message['text']
        text = text.split('\n')
        text[0] = '*'+str(normalize(user_data['day_str']))+'*'
        text[1] = '*'+str(user_data['time_str'])+'*'
        str_fin = ''
        for i in text:
            str_fin += i + '\n'
        action_keyboard = InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        item_change = InlineKeyboardButton('Изменить машину', callback_data=rewrite_rec.new(action_name='rewrite',
                                                                                            date=
                                                                                            user_data['day'],
                                                                                            time=
                                                                                            user_data['time'],
                                                                                            brand=user_data['callback_data'][
                                                                                                'brand'],
                                                                                            distant=
                                                                                            user_data['callback_data'][
                                                                                                'distant'],
                                                                                            group_data=
                                                                                            user_data['callback_data'][
                                                                                                'group_data']))
        item_change_date = InlineKeyboardButton('Изменить дату',
                                                callback_data=rewrite_date.new(action_name='rewrite_date',
                                                                              date=
                                                                              user_data['day'],
                                                                              time=
                                                                              user_data['time'],
                                                                              brand=user_data['callback_data'][
                                                                                  'brand'],
                                                                               distant=user_data['callback_data'][
                                                                                  'distant'],
                                                                              group_data=
                                                                              user_data['callback_data'][
                                                                                  'group_data']))
        action_keyboard.add(item_change, item_change_date)

        await bot.edit_message_text(chat_id=chat_to_send_id,
                                    text=str_fin,
                                    message_id=user_data['callback_data']['group_data'], parse_mode='Markdown')
        await bot.edit_message_text(chat_id=id_person,
                                    message_id=user_data['query'].message.message_id,
                                    text=str_fin,
                                    reply_markup=action_keyboard, parse_mode='Markdown')

        sheet = get_sheet("TO", "car info")
       # print(user_data['callback_data']['time'], user_data['callback_data']['date'])
        #print(user_data['time'], user_data['day'], user_data['callback_data']['brand'])
        sheet.update_cell(user_data['callback_data']['time'], user_data['callback_data']['date'], '')
        sheet.update_cell(user_data['time'], user_data['day'], user_data['callback_data']['brand'])
        await state.finish()