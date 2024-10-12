import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time

google_client = gspread.authorize(
    ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                     ["https://spreadsheets.google.com/feeds",
                                                     "https://www.googleapis.com/auth/drive"]))
google_sheet = google_client.open_by_url('https://docs.google.com/spreadsheets/d/1YeJyGttTkGCoNoXNvy3-5qJsR50WlvQ_hxf-RMM-JLM/edit')
sheet = google_sheet.worksheet('tests')

existing_user_ids = sheet.col_values(1)
# pprint(existing_user_ids[64:])

for i, value in enumerate(existing_user_ids, start=1):
    print(i, value)
    #sheet.update_cell(i, 1, f'=HYPERLINK("https://t.me/{value}", "{value}")')
    #time.sleep(1.5)
