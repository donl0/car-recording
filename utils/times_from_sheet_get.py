from utils.sheet_get import get_sheet


def get_times():
    sheet = get_sheet("TO", "car info")
    all_times = sheet.col_values(1)
    return all_times