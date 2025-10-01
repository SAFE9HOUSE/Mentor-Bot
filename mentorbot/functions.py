from consta import *


# функция, определяющая реакцию бота на команду start от пользователя
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    blockers = [
        'function_active', 
        'function_clear_list_active',
        'function_add_elem_list_active',
        'function_del_elem_list_active', 
        'function_send_message_option_active'
    ]
    

    if any(context.user_data.get(blocker, False) for blocker in blockers):
        await update.message.reply_text("Сейчас вы находитесь внутри блока команды /create_or_change. " 
                                        "Остальные функции вам не доступны. "
                                        "Завершите действие в /create_or_change для доступа к остальным функциям.")
    
    else:
        user = update.effective_user
        await update.message.reply_html(f"Привет, {user.mention_html()}! Я ментор бот. " 
                                        "Я создан, чтобы помогать тебе эффективно проводить свое время. " 
                                        "Добавь в мою базу список задач, которые ты бы хотел выполнять за день. "
                                        "Тогда я каждый день, в определенное время (настраиваемый параметр) буду присылать данный список, " 
                                        "напоминая о твоих задачах, помогая структурировать досуг. "
                                        "Для создания списка или его изменения напиши команду /create_or_change."
                                        "Также ты можешь написать /info для получения информации по всем командам, которые я знаю.")
       

# функция, определяющая реакцию бота на команду help от пользователя
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    blockers = [
        'function_active', 
        'function_clear_list_active',
        'function_add_elem_list_active',
        'function_del_elem_list_active', 
        'function_send_message_option_active'
    ]
    

    if any(context.user_data.get(blocker, False) for blocker in blockers):
         await update.message.reply_text("Сейчас вы находитесь внутри блока команды /create_or_change. "
                                         "Остальные функции вам не доступны. " 
                                         "Завершите действие в /create_or_change для доступа к остальным функциям.")
    
    else:
        await update.message.reply_text("Забыл кто я? Я ментор бот. "
                                        "Помогаю проводить день грамотно. " 
                                        "Начни с первого шага, используя /start, "
                                        "или переходи ко второму (/create_or_change) для создания или изменения списка задач.")


# функция, определяющая ошибку при работе бота
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    logger.error(f"Произошла ошибка: {context.error}", exc_info=context.error)
   
    if update and update.effective_message:
        await update.effective_message.reply_text("Извините, произошла ошибка.")


# функция создания (изменения) списка задач
async def create_daily_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    
    
    defaults = {
        'function_active': True,
        'function_clear_list_active': False,
        'function_add_elem_list_active': False,
        'function_del_elem_list_active': False,
        'function_send_message_option_active': False,
        'function_send_message_active': False,
        'score_time_option': 0,
        'send_hours': None,
        'send_minutes': None
    }
    
    
    for key, value in defaults.items():
        context.user_data[key] = value
    
    
    if 'tasks' not in context.user_data:
        context.user_data['tasks'] = []


    keyboard = [["Добавить элемент", "Удалить элемент"], 
                ["Напечатать список", "Очистить список"], 
                ["Установить время отправки", "Выход"]]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Отлично! У тебя есть 6 кнопок:\n\n"
        "• Первая добавляет элемент к списку\n\n"
        "• Вторая удаляет элемент из списка по названию\n\n"
        "• Третья печатает текущий список\n\n"
        "• Четвертая чистит весь список задач целиком\n\n"
        "• Пятая переходит к установке времени для посылки списка задач\n\n"
        "• Шестая выходит из блока команды\n\n"
        "Помни, что в список можно добавить не более 30 задач. Что будем делать?",
        reply_markup=reply_markup
    )


# функция получения информации о всех командах бота
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:


    blockers = [
        'function_active', 
        'function_clear_list_active',
        'function_add_elem_list_active',
        'function_del_elem_list_active', 
        'function_send_message_option_active'
    ]
    

    if any(context.user_data.get(blocker, False) for blocker in blockers):
         await update.message.reply_text("Сейчас вы находитесь внутри блока команды /create_or_change. "
                                         "Остальные функции вам не доступны. " 
                                         "Завершите действие в /create_or_change для доступа к остальным функциям.")
    
    else:
        await update.message.reply_text("Сводка по командам, которые я понимаю:\n\n"
                                        "\n• /start - начальная команда для знакомства с ботом\n" 
                                        "\n• /help - команда для напоминания пользователю, что бот из себя представляет\n"
                                        "\n• /create_or_change - создание или изменение списка задач " 
                                        "с последующим регулированием времени отправки\n"
                                        "\n• /stop - отключение ежедневной отправки списка задач\n"
                                        "\n• /info - получение информации о всех командах бота")
    




    