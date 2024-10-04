import gspread
import pandas as pd
import secret_data as secret
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def replace_digits_with_letters(input_number: int) -> str:
    return chr(65 + input_number)

def user_row(df: pd.DataFrame, t_id: str) -> str:
    return str(df[df[0] == t_id].index[0] + 1)

google_client = gspread.authorize(
    ServiceAccountCredentials.from_json_keyfile_name("credentials.json",
                                                     ["https://spreadsheets.google.com/feeds",
                                                     "https://www.googleapis.com/auth/drive"]))

google_sheet = google_client.open_by_url(secret.google_sheets_url)

users_sheet = google_sheet.worksheet('users')
users_headers= ['ID','NICKNAME','TELID','LOC','REGISTERED', 'TELUSERNAME', 'FNAME', 'LNAME', 'PHONE', 'EMAIL',	'FBID',	'STATUS']
def create_dict(headers):
    return {header: chr(65 + i) for i, header in enumerate(headers)}
uh = create_dict(users_headers)
print(uh)

# cal_sheet = google_sheet.worksheet('MEL 6/10')
cal_sheet_choosen = None
cal_headers= ['ID','NICKNAME', 'FNAME', 'LNAME', 'REGISTERED', 'PAYED', 'COMMENT']

# pprint(cal_sheet.col_values(1))
# df_users = pd.DataFrame(users_sheet.get_all_values())
# print(df_users)
# t_id = 't_012345'
# print(user_row(df_users, t_id))