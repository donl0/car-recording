#from sheet_get import get_sheet
import time
start_time = time.time()
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('silent-card-330316-7d0f47ab4f6b.json', scope)
client = gspread.authorize(creds)
print('нача')
sheet = client.open("TO")
sheet = sheet.worksheet("car info")
all_dates = sheet.row_values(1)
b=0
days_keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
days_keyboard.add("nazad")
item_today = InlineKeyboardButton(text='Сегодня')
days_keyboard.add(item_today)
for day in all_dates:
    item_day = InlineKeyboardButton(text=day)

    days_keyboard.add(item_day)
for i in range(20):
    b+=1
    print(b)
print(all_dates)
print("--- %s seconds ---" % (time.time() - start_time))