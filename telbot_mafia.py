from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
import telbot_globals as gl

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
    question_index, answer = query.data.split(',')
    question_index = int(question_index)
    option_index = gl.questions[question_index]["options"].index(answer)
    gl.user_answers[query.message.chat.id].append(gl.questions[question_index]["options"][option_index])
    if question_index + 1 < len(gl.questions):
        await ask_question(query, question_index + 1)
    else:
        await query.message.reply_text(f"Ваши ответы: {', '.join(gl.user_answers[query.message.chat.id])}")

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
    application = Application.builder().token(gl.secret.tel_bot_token).build()
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()