from aiogram import Bot, Dispatcher
from aiogram import types
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from settings.config import chat_to_send_id
from utils.get_time_ccel import from_your_time_to_cell
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard
from utils.logic import rewrite_rec, rewrite_date
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

async def to_handler(bot: Bot, dp: Dispatcher):
    @dp.message_handler(lambda message: message.text == 'ТО', lambda message: message['chat']['type']!='supergroup')
    async def get_to(message: types.Message):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Выберите день', reply_markup=days_keyboard())
        await message.reply(text='Выберите день', reply_markup=days_keyboard())
        await OrderDataUser.day_wait.set()

    @dp.message_handler(state=OrderDataUser.day_wait)
    async def get_day(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        sheet = get_sheet("TO", "car info")
        all_dates = sheet.row_values(1)
        mass_for_new_items = all_dates.copy()
        mass_for_new_items.append('Сегодня')
        if message.text in mass_for_new_items:
            id_person = message.chat.id
            day_cell = get_day_num_cell(message.text)
            await state.update_data(day=day_cell)
            await state.update_data(day_str=message.text)
            await OrderDataUser.time_wait.set()
            #await bot.send_message(chat_id=id_person, text='Выберите время', reply_markup=times_keyboard())
            await message.reply(text='Выберите время', reply_markup=times_keyboard(day_cell))
        else:
            await bot.send_message(chat_id=id_person,
                                   text='https://docs.google.com/spreadsheets/d/1C5YqE3QYlte15z6OsKF_cSVs-A9HxAkDIRs9oPQG--w/edit?usp=sharing',
                                   reply_markup=to_keyboard)
            await state.finish()
    @dp.message_handler(state=OrderDataUser.time_wait)
    async def get_time_for_sheep(message: types.Message, state: FSMContext):
        id_person = message.chat.id

        await state.update_data(time=from_your_time_to_cell(message.text))
        await state.update_data(time_str=message.text)
        #await bot.send_message(chat_id=id_person, text='Введите название машины', reply_markup=back_keyboard)
        await message.reply(text='Введите название машины', reply_markup=back_keyboard)
        await OrderDataUser.brand_wait.set()

    @dp.message_handler(lambda message: message.text != 'Назад', state=OrderDataUser.brand_wait)
    async def get_car_name(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await state.update_data(brand=message.text)
        #await bot.send_message(chat_id=id_person, text='Введите пробег авто', reply_markup=back_keyboard)
        await message.reply(text='Введите пробег авто', reply_markup=back_keyboard)
        await OrderDataUser.distant_of_car.set()

    @dp.message_handler(lambda message: message.text != 'Назад', state=OrderDataUser.distant_of_car)
    async def get_car_brand(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await state.update_data(distant=message.text)
        #await bot.send_message(chat_id=id_person, text='Какое действие', reply_markup=actions_with_car_keybard())
        await message.reply(text='Какое действие', reply_markup=actions_with_car_keybard())
        await OrderDataUser.action_wait.set()

    @dp.message_handler(lambda message: message.text != 'Назад', state=OrderDataUser.action_wait)
    async def get_action(message: types.Message, state: FSMContext):
        id_person = message.chat.id

        await state.update_data(action=message.text)
        if message.text == 'Ремонт':
            await OrderDataUser.action_type_wait.set()
            await message.reply(text='Напишите какой именно ремонт')
        else:
            user_data = await state.get_data()
            sheet = get_sheet("TO", "car info")
            sheet.update_cell(user_data['time'], user_data['day'], user_data['brand'])

            string = ''
            mass_data = [normalize(user_data['day_str']), user_data['time_str'], user_data['brand'], user_data['distant'], user_data['action']]
            for mess in mass_data:
                string += '*'+str(mess)+'*\n'
            string += '(' + str(message['from']['first_name']) + ' '
            try:
                string += str(message['from']['last_name'])+')'
            except:
                pass
            group_mess = await bot.send_message(chat_id=chat_to_send_id, text=string,
                                                parse_mode='Markdown')
            group_mess_id = group_mess.message_id
            action_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
            item_change = InlineKeyboardButton('Изменить машину', callback_data=rewrite_rec.new(action_name='rewrite',
                                                                                                date=user_data['day'],
                                                                                                time=user_data['time'],
                                                                                                distant=user_data['distant'],
                                                                                                brand=user_data[
                                                                                                    'brand'],
                                                                                                group_data=group_mess_id))
            item_change_date = InlineKeyboardButton('Изменить дату',
                                                    callback_data=rewrite_date.new(action_name='rewrite_date',
                                                                                   date=user_data['day'],
                                                                                   brand=user_data['brand'],
                                                                                   time=user_data['time'],
                                                                                   distant=user_data['distant'],
                                                                                   group_data=group_mess_id))
            action_keyboard.add(item_change, item_change_date)
            await message.reply(text=string, parse_mode='Markdown', reply_markup=action_keyboard)
            await bot.send_message(chat_id=id_person, text='бд обновлена', reply_markup=to_keyboard,
                                   parse_mode='Markdown')

            await state.finish()

    @dp.message_handler(lambda message: message.text != 'Назад', state=OrderDataUser.action_type_wait)
    async def get_action(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await state.update_data(action_type=message.text)
        user_data = await state.get_data()
        sheet = get_sheet("TO", "car info")
        sheet.update_cell(user_data['time'], user_data['day'], user_data['brand'])

        string = ''
        mass_data = [normalize(user_data['day_str']), user_data['time_str'], user_data['brand'], user_data['distant'],
                     user_data['action'], user_data['action_type']]
        for mess in mass_data:
            string += '*' + str(mess) + '*\n'
        string += '(' + str(message['from']['first_name']) + ' '
        try:
            string += str(message['from']['last_name'])+')'
        except:
            pass
        #в беседу
        group_mess = await bot.send_message(chat_id=chat_to_send_id, text=string,
                               parse_mode='Markdown')
        group_mess_id = group_mess.message_id
        action_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
        item_change = InlineKeyboardButton('Изменить машину', callback_data=rewrite_rec.new(action_name='rewrite',
                                                                                     date=user_data['day'],
                                                                                     time=user_data['time'],
                                                                                     brand=user_data['brand'],
                                                                                            distant=user_data[
                                                                                                'distant'],
                                                                                     group_data=group_mess_id))
        item_change_date = InlineKeyboardButton('Изменить дату', callback_data=rewrite_date.new(action_name='rewrite_date',
                                                                                            date=user_data['day'],
                                                                                            brand=user_data['brand'],
                                                                                            time=user_data['time'],
                                                                                                distant=user_data[
                                                                                                    'distant'],
                                                                                            group_data=group_mess_id))
        action_keyboard.add(item_change, item_change_date)
        await message.reply(text=string, parse_mode='Markdown', reply_markup=action_keyboard)
        await bot.send_message(chat_id=id_person, text='бд обновлена', reply_markup=to_keyboard,
                               parse_mode='Markdown')

        await state.finish()
