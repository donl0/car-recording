from settings.client_connect import client

def get_sheet(table_name, page):
    sheet = client.open(table_name)
    sheet = sheet.worksheet(page)
    return sheet