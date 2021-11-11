from datetime import datetime

from utils.sheet_get import get_sheet


def get_day_num_cell(day):
    if day == 'Сегодня':
        nowday = normalize(day)
    else:
        nowday = day
    return make_cell(nowday)


def normalize(day):
    if day == 'Сегодня':
        current_datetime = datetime.now()
        day = current_datetime.day
        mounth = current_datetime.month
        year = current_datetime.year
        if int(day) < 10:
            day = '0'+str(day) + '.' + str(mounth)+'.'+str(year)
        else:
            day = str(day) + '.' + str(mounth) + '.' + str(year)
    return day


def make_cell(nowday):
    sheet = get_sheet("TO", "car info")
    all_dates = sheet.row_values(1)
    cell_num = 0
    for date in all_dates:
        cell_num += 1
        if date == nowday:
            break
    return cell_num


def get_all_days():
    sheet = get_sheet("TO", "car info")
    all_dates = sheet.row_values(1)
    #print(type(all_dates))
    return all_dates


def get_all_days_with_new_items():
    sheet = get_sheet("TO", "car info")
    all_dates = sheet.row_values(1)
    mass_for_new_items = all_dates.copy()
    mass_for_new_items.append('Сегодня')
    return mass_for_new_items