from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from utils.get_day import get_all_days
from utils.times_from_sheet_get import get_times
from utils.sheet_get import get_sheet
item_back = InlineKeyboardButton(text='Назад')
item_cancel = InlineKeyboardButton(text='Отменить всё')

to_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
item_to = InlineKeyboardButton(text='ТО')
item_clear = InlineKeyboardButton(text='Удалить запись')
to_keyboard.add(item_to, item_clear)



back_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
back_keyboard.add(item_back)


def times_keyboard(day_cell):
    times_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    times_keyboard.add(item_back)
    #нам нужно узнать свободные ячейки
    many_times = get_times()
    i = 0
    sheet = get_sheet("TO", "car info")
    for time in many_times:
        i += 1
        val = sheet.cell(i, day_cell).value
        if val == None:
            item_time = InlineKeyboardButton(text=time)
            times_keyboard.add(item_time)

    return times_keyboard


def days_keyboard():
    days = get_all_days()
    days_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    days_keyboard.add(item_back)
    item_today = InlineKeyboardButton(text='Сегодня')
    days_keyboard.add(item_today)
    for day in days:
        item_day = InlineKeyboardButton(text=day)

        days_keyboard.add(item_day)
    return days_keyboard


def actions_with_car_keybard():
    action_keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    action_keyboard.add(item_back)
    item_to = InlineKeyboardButton(text='ТО')
    item_repair = InlineKeyboardButton(text='Ремонт')
    action_keyboard.add(item_to, item_repair)
    return action_keyboard