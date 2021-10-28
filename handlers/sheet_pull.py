from aiogram import Bot, Dispatcher
from aiogram import types
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from utils.get_time_ccel import from_your_tim_to_cell
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times


async def to_handler(bot: Bot, dp: Dispatcher):
    @dp.message_handler(text='ТО')
    async def get_to(message: types.Message):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Выберите день', reply_markup=days_keyboard())
        await message.reply(text='Выберите день', reply_markup=days_keyboard())
        await OrderDataUser.day_wait.set()

    @dp.message_handler(text=get_all_days_with_new_items(), state=OrderDataUser.day_wait)
    async def get_day(message: types.Message, state: FSMContext):
        print(get_all_days_with_new_items())
        id_person = message.chat.id
        await state.update_data(day=message.text)
        await OrderDataUser.time_wait.set()
        #await bot.send_message(chat_id=id_person, text='Выберите время', reply_markup=times_keyboard())
        await message.reply(text='Выберите время', reply_markup=times_keyboard())

    @dp.message_handler(text=get_times(), state=OrderDataUser.time_wait)
    async def get_time_for_sheep(message: types.Message, state: FSMContext):
        id_person = message.chat.id

        await state.update_data(time=message.text)
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
        user_data = await state.get_data()
        sheet = get_sheet("TO", "car info")
        print(from_your_tim_to_cell(user_data['time']))
        print(get_day_num_cell(user_data['time']))
        print(user_data['brand'])
        sheet.update_cell(from_your_tim_to_cell(user_data['time']), get_day_num_cell(user_data['day']), user_data['brand'])

        num = 0
        string = ''
        mass_data = [normalize(user_data['day']), user_data['time'], user_data['brand'], user_data['distant'], user_data['action']]
        for mess in mass_data:
            num += 1
            string += str(num)+'. *'+mess+'*\n'
        await message.reply(text=string, parse_mode='Markdown', reply_markup=to_keyboard)
        await state.finish()
        #await bot.send_message(chat_id=id_person, text='Какое действие', reply_markup=actions_with_car_keybard())
     #   await OrderDataUser.action_wait.set()