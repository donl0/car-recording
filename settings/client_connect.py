import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('settings/silent-card-330316-7d0f47ab4f6b.json', scope)
client = gspread.authorize(creds)