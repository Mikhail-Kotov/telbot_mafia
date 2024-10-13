import json
import locale
import re
import time
from base64 import b64decode
from datetime import date, timedelta


# current time in string format
def ct() -> str:
    return str(time.strftime('%Y-%m-%d %H:%M:%S'))

def replace_digits_with_letters(input_number: int) -> str:
    return chr(65 + input_number)

def generate_sundays(current_date: date, last_date: date) -> list:
    sundays = []
    while current_date <= last_date:
        if current_date.weekday() == 6:  # 6 is Sunday
            sundays.append(current_date.strftime("%-d %B %Y"))
        current_date += timedelta(days=1)
    return sundays

def generate_next_sunday() -> date:
    today = date.today()
    days_until_sunday = 6 - today.weekday()
    if days_until_sunday < 0:
        days_until_sunday += 7
    return today + timedelta(days=days_until_sunday)

def decode(s: str) -> str:
    return str(b64decode(s), "utf-8")

# функция заменяет "6 октября 2024" в "6/10" отбрасывая год
def replace_russian_date(date_str: str) -> str:
    months = {'января': '1', 'февраля': '2', 'марта': '3', 'апреля': '4',
              'мая': '5', 'июня': '6', 'июля': '7', 'августа': '8',
              'сентября': '9', 'октября': '10', 'ноября': '11', 'декабря': '12'}

    pattern = r'(\d{1,2})\s(\w+)\s\d{4}'
    match = re.search(pattern, date_str)

    if match:
        day = match.group(1)
        month = months.get(match.group(2).lower())
        if month:
            return f"{day}/{month}"

def replace_russian_words(text):
    replacements = {"Да": "Yes", "Нет": "No"}
    for word, replacement in replacements.items():
        text = text.replace(word, replacement)
    return text


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

# tel_api           through - https://core.telegram.org/api/obtaining_api_id
# tel_bot_token(s)  through - @BotFather
secret = json.load(open('.config/telbot_credentials.json', 'r'))
secret["tel_api_id"], secret["tel_api_hash"] = decode(secret["tel_api_enc"]).split(':')
secret["tel_bot_token"] = decode(secret["tel_bot_token_enc"])
secret["tel_mmc_reg_bot_token"] = decode(secret["tel_mmc_reg_bot_token_enc"])

# start_date = date(2024, 10, 1)
# end_date   = date(2024, 11, 1)
start_date = generate_next_sunday()
end_date   = start_date + timedelta(days=28)

# greetings = ["Это бот для записи на игру МАФИЯ в Мельбурне. Для начала нажмите /start"]

questions = [{"question": "На какую дату игры вы хотели бы записаться?", "options": generate_sundays(start_date, end_date)},
             {"question": "Произвели ли вы уже оплату на эту дату или готовы произвести её прямо сейчас?", "options": ["Да", "Нет"]}]

questions_reg = [{"question": "Регистрировались ли вы ранее через web-форму или с другого телеграма?", "options": ["Да", "Нет"]},
                 {"question": "Желаете указать ваш nickname в игре?", "options": ["", "не в данный момент"]},
                 {"question": "Желаете указать дополнительную информацию (имя, email, телефон)?", "options": ["Да", "Нет"]}]

user_answers = dict()

tel_client = None
df_users = None  # for pandas dataframe



