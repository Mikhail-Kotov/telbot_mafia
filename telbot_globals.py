import locale
import logging
from datetime import date, timedelta
from telethon import TelegramClient
import secret_data as secret

def generate_sundays(current_date: date, last_date: date) -> list:
    sundays = []
    while current_date <= last_date:
        if current_date.weekday() == 6:  # 6 is Sunday
            sundays.append(current_date.strftime("%-d %B %Y"))
        current_date += timedelta(days=1)
    return sundays

def generate_next_sunday():
    today = date.today()
    days_until_sunday = 6 - today.weekday()
    if days_until_sunday < 0:
        days_until_sunday += 7
    return today + timedelta(days=days_until_sunday)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# start_date = date(2024, 10, 1)
# end_date   = date(2024, 11, 1)
start_date = generate_next_sunday()
end_date   = start_date + timedelta(days=28)

questions = [{"question": "На какую дату игры вы хотели бы записаться?", "options": generate_sundays(start_date, end_date), },
             {"question": "Произвели ли вы уже оплату на эту дату или готовы произвести её прямо сейчас?", "options": ["Да", "Нет"]}]
user_answers = dict()

tel_client = TelegramClient('session_name', int(secret.tel_api_id), secret.tel_api_hash)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)