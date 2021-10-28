from aiogram import Bot, Dispatcher
from aiogram import types
#from ...utils.states import OrderDataUser, FSMContext, State
from settings.client_connect import client
from utils.get_time_ccel import from_your_time_to_cell
from utils.get_day import get_day_num_cell, get_all_days, normalize, get_all_days_with_new_items
from utils.keyboards import actions_with_car_keybard, times_keyboard, days_keyboard, to_keyboard, back_keyboard, times_keyboard2
from utils.sheet_get import get_sheet
from utils.states import OrderDataUser, FSMContext
from utils.times_from_sheet_get import get_times


async def clear_cell_handler(bot: Bot, dp: Dispatcher):
    @dp.message_handler(text='Удалить запись')
    async def get_to(message: types.Message):
        id_person = message.chat.id
        #await bot.send_message(chat_id=id_person, text='Выберите день', reply_markup=days_keyboard())
        await message.reply(text='Выберите день', reply_markup=days_keyboard())
        await OrderDataUser.day_wait2.set()

    @dp.message_handler(text=get_all_days_with_new_items(), state=OrderDataUser.day_wait2)
    async def get_day(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        day_cell = get_day_num_cell(message.text)
        await state.update_data(day=day_cell)
        await state.update_data(day_str=message.text)
        await OrderDataUser.time_wait2.set()
        # await bot.send_message(chat_id=id_person, text='Выберите время', reply_markup=times_keyboard())
        await message.reply(text='Выберите время', reply_markup=times_keyboard2(day_cell))

    @dp.message_handler(lambda message: message.text != 'Назад', state=OrderDataUser.time_wait2)
    async def get_action(message: types.Message, state: FSMContext):
        id_person = message.chat.id
        await state.update_data(time_str=message.text)
        await state.update_data(time=from_your_time_to_cell(message.text))
        user_data = await state.get_data()
        sheet = get_sheet("TO", "car info")
        car_num = sheet.cell(user_data['time'], user_data['day']).value
        sheet.update_cell(user_data['time'], user_data['day'], '')

        num = 0
        string = ''
        mass_data = [normalize(user_data['day_str']), user_data['time_str']]
        for mess in mass_data:
            num += 1
            string += str(num) + '. *' + str(mess) + '*\n'
        string += str('3. *')+car_num+'*\n'
        string += 'Запись удалена\n'
        string += '('+str(message['from']['first_name'])+' '
        try:
            string +=str(message['from']['last_name'])+')'
        except:
            pass
        await message.reply(text=string, parse_mode='Markdown', reply_markup=to_keyboard)
        await bot.send_message(chat_id='-1001728784459', text=string, reply_markup=actions_with_car_keybard(), parse_mode='Markdown')
        await state.finish()