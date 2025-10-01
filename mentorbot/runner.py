from consta import *
from functions import start, help_command, info_command, error_handler, create_daily_message
from handle_buttons_function import handle_buttons, stop_send_daily_message


# функция запуска бота
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    
    application.add_handler(CommandHandler("create_or_change", create_daily_message))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    application.add_handler(CommandHandler("stop", stop_send_daily_message))
    
    application.add_error_handler(error_handler)

    logger.info("Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# запуск бота 
if __name__ == "__main__":
    main()
