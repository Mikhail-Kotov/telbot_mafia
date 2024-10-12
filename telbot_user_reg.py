import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import telbot_globals as gl


async def get_user_info(user_id) -> str:
    async with gl.tel_client:
        return await gl.tel_client.get_entity(user_id)


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = await get_user_info(user_id)
    print(f'{user.first_name} {user.last_name} @{user.username} {user.phone}')
    await update.message.reply_text(f"Приветствую вас {user.first_name} {user.last_name} @{user.username} {user.phone}!\n"
                                    f"Это бот для регистрации в группе MELBOURNE MAFIA CLUB и дальнейшей записи на игру МАФИЯ в конкретный день.")

    keyboard = [
        [InlineKeyboardButton("Да", callback_data='registered_yes')],
        [InlineKeyboardButton("Нет", callback_data='registered_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Регистрировались ли вы ранее через web-форму или с другого телеграма?', reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'registered_yes':
        await query.edit_message_text(text="Пожалуйста, сообщите админу группы об этом.")
    elif query.data == 'registered_no':
        await query.edit_message_text(text="Какой вы хотели бы получить никнейм в игре МАФИЯ?")
        context.user_data['awaiting_nickname'] = True


async def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('awaiting_nickname'):
        context.user_data['nickname'] = update.message.text
        context.user_data['awaiting_nickname'] = False
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='details_yes')],
            [InlineKeyboardButton("Нет", callback_data='details_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Желаете ли вы уточнить дополнительные детали?', reply_markup=reply_markup)
    elif context.user_data.get('awaiting_details'):
        context.user_data['details'].append(update.message.text)
        if len(context.user_data['details']) < 4:
            await update.message.reply_text(context.user_data['questions'][len(context.user_data['details'])])
        else:
            context.user_data['awaiting_details'] = False
            details = context.user_data['details']
            await update.message.reply_text(f"Ваши данные:\nИмя: {details[0]}\nФамилия: {details[1]}\nТелефон: {details[2]}\nEmail: {details[3]}")


# Обработка ответов на вопрос о дополнительных деталях
async def details_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'details_yes':
        context.user_data['awaiting_details'] = True
        context.user_data['details'] = []
        context.user_data['questions'] = [
            "Введите ваше имя:",
            "Введите вашу фамилию:",
            "Введите ваш телефон:",
            "Введите ваш email:"
        ]
        await query.edit_message_text(text=context.user_data['questions'][0])
    elif query.data == 'details_no':
        await query.edit_message_text(text="Спасибо! Ваши данные сохранены.")


def main() -> None:
    application = Application.builder().token(gl.secret['tel_mmc_reg_bot_token']).build()
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    application.add_handler(CommandHandler(["start"], start))

    application.add_handler(CallbackQueryHandler(button, pattern='^registered_'))
    application.add_handler(CallbackQueryHandler(details_button, pattern='^details_'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
