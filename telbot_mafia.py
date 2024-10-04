from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
import logging
import pandas as pd
from telethon import TelegramClient
import secret_data as secret

import telbot_globals as gl
import gs

async def get_user_id_by_phone(phone_number):
    async with gl.tel_client:
        user = await gl.tel_client.get_entity(phone_number)
        print(f'ID пользователя: {user.id}')

async def get_user_info(user_id):
    async with gl.tel_client:
        return await gl.tel_client.get_entity(user_id)

async def ask_question(query, question_index: int) -> None:
    question = gl.questions[question_index]
    keyboard = [[InlineKeyboardButton(option, callback_data=f"{question_index},{option}")
                 for option in question["options"][i:i+2]] for i in range(0, len(question["options"]), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(question["question"], reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    t_id = query.message.chat.id
    st_id = 't_' + str(query.message.chat.id)
    tr = gs.user_row(gl.df_users, st_id) # t_id row number on google sheet users
    question_index, answer = query.data.split(',')
    question_index = int(question_index)
    option_index = gl.questions[question_index]["options"].index(answer)
    gl.user_answers[t_id].append(gl.questions[question_index]["options"][option_index])

    if question_index + 1 < len(gl.questions):
        await ask_question(query, question_index + 1)
    else:
        await query.message.reply_text(f"Ваши ответы: {', '.join(gl.user_answers[t_id])}")
        # =HYPERLINK("#gid=0&range=A19", users!A19)
        gs.cal_sheet_choosen = gs.google_sheet.worksheet('MEL ' + gl.replace_russian_date(gl.user_answers[t_id][0]))

        new_row = [f'=HYPERLINK("#gid=0&range={gs.uh["ID"]}{tr}", "{st_id}")',
                   f'=users!{gs.uh["NICKNAME"]}{tr}',
                   f'=users!{gs.uh["FNAME"]}{tr}',
                   f'=users!{gs.uh["LNAME"]}{tr}',
                   gl.ct(),
                   gl.replace_russian_words(gl.user_answers[t_id][1]), "комментарий 2"]
        existing_user_ids = gs.cal_sheet_choosen.col_values(1)
        print(existing_user_ids)
        if st_id not in existing_user_ids:
            print("Строка добавлена", new_row)
            print(gs.cal_sheet_choosen.append_row(new_row, value_input_option="USER_ENTERED"))
        else:
            print("Первое поле уже существует в таблице")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    user_id = update.effective_user.id
    user = await get_user_info(user_id)
    print(f'{user.first_name} {user.last_name} @{user.username} {user.phone}')
    await update.message.reply_text(f"Приветствую вас {user.first_name} {user.last_name} @{user.username} !\n"
                                    f"Это бот для записи на игру МАФИЯ в Мельбурне.") # {user.phone}
    chat_id = update.message.chat_id
    gl.user_answers[chat_id] = []
    await ask_question(update, 0)

def main() -> None:
    gl.tel_client = TelegramClient('session_name', int(gl.secret.tel_api_id), gl.secret.tel_api_hash)
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

    gl.df_users = pd.DataFrame(gs.users_sheet.get_all_values())
    application = Application.builder().token(gl.secret.tel_bot_token).build()
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()