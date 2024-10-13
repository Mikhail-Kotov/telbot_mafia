import json
import gspread
import pandas as pd
from base64 import b64decode
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def replace_digits_with_letters(input_number: int) -> str:
    return chr(65 + input_number)

def user_row(df: pd.DataFrame, t_id: str) -> str:
    return str(df[df[0] == t_id].index[0] + 1)

def decode(s: str) -> str:
    return str(b64decode(s), "utf-8")

def create_dict(headers: list) -> dict:
    return {header: chr(65 + i) for i, header in enumerate(headers)}

google_client = gspread.authorize(
    ServiceAccountCredentials.from_json_keyfile_name(".config/gsheet_credentials.json",
                                                     ["https://spreadsheets.google.com/feeds",
                                                      "https://www.googleapis.com/auth/drive"]))
secret = json.load(open('.config/telbot_credentials.json', 'r'))
secret['google_sheets_url'] = decode(secret['google_sheets_url_enc'])

google_sheet = google_client.open_by_url(secret['google_sheets_url'])
users_sheet = google_sheet.worksheet('users')

#                A    B          C       D     E             F              G        H        I        J         K       L
users_headers= ['ID','NICKNAME','TELID','LOC','REGISTERED', 'TELUSERNAME', 'FNAME', 'LNAME', 'PHONE', 'EMAIL',	'FBID',	'STATUS']
uh = create_dict(users_headers)

#              A    B           C        D        E             F          G         H        I          J
cal_headers= ['ID','NICKNAME', 'FNAME', 'LNAME', 'REGISTERED', 'UPDATED', 'COMING', 'PAYED', 'COMMENT', 'MTIME']
cal_sheet_choosen = None

# cal_sheet = google_sheet.worksheet('MEL 6/10')
# pprint(cal_sheet.col_values(1))
# df_users = pd.DataFrame(users_sheet.get_all_values())
# print(df_users)
# t_id = 't_394944528'
# print(user_row(df_users, t_id))