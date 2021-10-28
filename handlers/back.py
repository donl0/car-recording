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


async def back_handler(bot: Bot, dp: Dispatcher):
    @dp.message_handler(text='Назад', state=OrderDataUser.day_wait)
    async def back_from_get_to(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await bot.send_message(chat_id=id_person, text='https://docs.google.com/spreadsheets/d/1C5YqE3QYlte15z6OsKF_cSVs-A9HxAkDIRs9oPQG--w/edit?usp=sharing', reply_markup=to_keyboard)
        await state.finish()

    @dp.message_handler(text='Назад', state=OrderDataUser.time_wait)
    async def back_from_get_day(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Выберите день', reply_markup=days_keyboard())
        await message.reply(text='Выберите день', reply_markup=days_keyboard())
        await OrderDataUser.day_wait.set()

    @dp.message_handler(text='Назад', state=OrderDataUser.brand_wait)
    async def back_from_get_car_name(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await OrderDataUser.time_wait.set()
        # await bot.send_message(chat_id=id_person, text='Выберите время', reply_markup=times_keyboard())
        await message.reply(text='Выберите время', reply_markup=times_keyboard())

    @dp.message_handler(text='Назад', state=OrderDataUser.distant_of_car)
    async def back_from_get_car_brand(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Введите пробег авто')
        await message.reply(text='Введите название машины', reply_markup=back_keyboard)
        await OrderDataUser.brand_wait.set()

    @dp.message_handler(text='Назад', state=OrderDataUser.action_wait)
    async def back_from_get_action(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Какое действие', reply_markup=actions_with_car_keybard())
        await message.reply(text='Введите пробег авто', reply_markup=back_keyboard)
        await OrderDataUser.distant_of_car.set()
