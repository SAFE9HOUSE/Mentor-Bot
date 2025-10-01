from consta import *
from functions import create_daily_message


# функция реакции бота на определенные сообщения (в зависимости от состояния)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    text = update.message.text
    
    
    blockers = [
        'function_active', 
        'function_clear_list_active',
        'function_add_elem_list_active',
        'function_del_elem_list_active', 
        'function_send_message_option_active'
    ]
   
    
    if not any(context.user_data.get(blocker) for blocker in blockers):
        await update.message.reply_text("Функция /create_or_change не активна. Текстовые сообщения игнорируются.")
    
      
    elif context.user_data.get('function_active'):
        match text:
            case "Добавить элемент":
                context.user_data['function_active'] = False
                context.user_data['function_add_elem_list_active']  = True
                reply_markup = ReplyKeyboardMarkup([["Напечатай список"], ["Хочу вернуться назад"]], resize_keyboard=True)
                await update.message.reply_text("Напишите, что вы хотите добавить (каждое сообщение - элемент для добавления)", 
                                                reply_markup=reply_markup)

            case "Удалить элемент":
                tasks = context.user_data.get('tasks', [])

                if tasks:
                    context.user_data['function_active'] = False
                    context.user_data['function_del_elem_list_active'] = True
                    reply_markup = ReplyKeyboardMarkup([["Напечатай список"], ["Хочу вернуться назад"]], resize_keyboard=True)
                    await update.message.reply_text("Напишите, что вы хотите удалить (каждое сообщение - элемент для удаления)", 
                                                    reply_markup=reply_markup)
                
                else:
                    await update.message.reply_text("Список задач пуст, удалять нечего")
    
            case "Напечатать список":
                tasks = context.user_data.get('tasks', [])
                
                if tasks:
                    tasks_text = "Ваш текущий список:\n" + "\n".join(f"• {task}" for task in tasks)
                
                else:
                    tasks_text = "Ваш список задач пуст"
                
                await update.message.reply_text(tasks_text)
    
            case "Очистить список":
                tasks = context.user_data.get('tasks', [])
                
                if tasks:
                    context.user_data['function_active'] = False
                    context.user_data['function_clear_list_active'] = True
                    reply_markup = ReplyKeyboardMarkup([["Да", "Нет, вернуться назад"]], resize_keyboard=True)
                    await update.message.reply_text("Вы действительно хотите очистить список?", reply_markup=reply_markup)
                
                else:
                    await update.message.reply_text("Ваш список и так пуст")
                
            case "Установить время отправки":
                tasks = context.user_data.get('tasks', [])

                if tasks:
                    await update.message.reply_text("Едем дальше")
                    context.user_data['function_active'] = False
                    context.user_data['function_send_message_option_active'] = True
                    reply_markup = ReplyKeyboardMarkup([["Отправить запрос", "Вернуться назад"], 
                                                        ["Вывести планируемое время отправки"], ["Сбросить время отправки"]], 
                                                        resize_keyboard=True)
                    
                    await update.message.reply_text("Сейчас введи часы и минуты для ежедневной отправки списка задач. "
                                                    "Вводить нужно каждую опцию отдельным сообщением. "
                                                    "Помни, что часовой пояс по умолчанию - Europe/Moscow", reply_markup=reply_markup)
                
                else:
                    await update.message.reply_text("Сначала добавь что-то в список")
    
            case "Выход":
                context.user_data['function_active'] = False
                
                await update.message.reply_text("Вы вышли из блока", reply_markup=ReplyKeyboardRemove())
    
            case _:
                await update.message.reply_text("Ваша команда некорректна")
    
    
    elif context.user_data.get('function_clear_list_active'):
        match text:
            case "Да":
                context.user_data['tasks'] = []
                await update.message.reply_text("Список очищен!")
                reply_markup=ReplyKeyboardRemove()
                await create_daily_message(update, context)
            
            case "Нет, вернуться назад":
                reply_markup=ReplyKeyboardRemove()
                await create_daily_message(update, context)
            
            case _:
                await update.message.reply_text("Ваша команда некорректна")
    
    
    elif context.user_data.get('function_add_elem_list_active'):
        match text:
            case "Напечатай список":
                tasks = context.user_data.get('tasks', [])
                
                if tasks:
                    tasks_text = "Ваш текущий список:\n" + "\n".join(f"• {task}" for task in tasks)
                
                else:
                    tasks_text = "Ваш список задач пуст"
                
                await update.message.reply_text(tasks_text)

            case "Хочу вернуться назад":
                reply_markup=ReplyKeyboardRemove()
                await create_daily_message(update, context)
            
            case _:
                if text not in context.user_data['tasks'] and len(context.user_data['tasks']) < 30:
                    context.user_data['tasks'].append(text)
                    await update.message.reply_text("Элемент успешно добавлен в список")
                
                else:
                    await update.message.reply_text("Длина списка переполнена или ваш текст совпадает с текстом элемента из списка")
    

    elif context.user_data.get('function_del_elem_list_active'):
        match text:
            case "Напечатай список":
                tasks = context.user_data.get('tasks', [])
                
                if tasks:
                    tasks_text = "Ваш текущий список:\n" + "\n".join(f"• {task}" for task in tasks)
                
                else:
                    tasks_text = "Ваш список задач пуст"
                
                await update.message.reply_text(tasks_text)
            
            case "Хочу вернуться назад":
                reply_markup=ReplyKeyboardRemove()
                await create_daily_message(update, context)
            
            case _:
                if text not in context.user_data['tasks']:
                    await update.message.reply_text("Такого элемента в списке нет, удаление невозможно")
                
                else:
                    context.user_data['tasks'].remove(text)
                    await update.message.reply_text("Элемент успешно удален из списка")
    
    
    elif context.user_data.get('function_send_message_option_active'):
        match text:
            case "Отправить запрос":
                if context.user_data['send_hours'] != None and context.user_data['send_minutes'] != None:
                    
                    
                    tasks = context.user_data.get('tasks', [])
                    tasks_text = "Добрый день! Ваш список задач на сегодня :\n\n" + "\n".join(f"• {task}" for task in tasks) + "\n\nУдачи! Все получится!"
                    
                    target_time = datetime.time(hour=context.user_data['send_hours'], 
                                                minute=context.user_data['send_minutes'],
                                                second=0, 
                                                tzinfo=ZoneInfo(TARGET_TIMEZONE))
                    
                    chat_id = update.effective_chat.id
                    job_name = f"daily_reminder_{chat_id}"

                    current_jobs = context.job_queue.get_jobs_by_name(job_name)
                    for job in current_jobs:
                        job.schedule_removal()


                    context.job_queue.run_daily(
                         send_daily_reminder,  
                         target_time,          
                         name=job_name,        
                         chat_id=chat_id,
                         data = tasks_text      
                    )    
                    
                    await update.message.reply_text(f"Ежедневное напоминание установлено на {target_time.strftime('%H:%M')}. "
                                                    "Вы будете получать ваш список задач каждый день в это время. "
                                                    "Чтобы отключить ежедневное напоминание, введите /stop. "
                                                    "Помните, что если вы хотите указать иное время, или иной список задач, "
                                                    "вам придется пройти этот цикл заново.")

                    context.user_data['function_active'] = False
                    context.user_data['function_send_message_option_active'] = False
                    await update.message.reply_text("Вы вышли из блока", reply_markup=ReplyKeyboardRemove())
                    
                else:
                    await update.message.reply_text("Операция невозможна. Вы не заполнили временные данные для отправки списка задач.")

            case "Вернуться назад":
                reply_markup=ReplyKeyboardRemove()
                await create_daily_message(update, context)
            
            case "Вывести планируемое время отправки":
                if context.user_data['send_hours'] != None and context.user_data['send_minutes'] != None:
                     
                     target_time = datetime.time(hour=context.user_data['send_hours'], 
                                                 minute=context.user_data['send_minutes'],
                                                 second=0, 
                                                 tzinfo=ZoneInfo(TARGET_TIMEZONE))
                     
                     await update.message.reply_text(f"Ежедневное сообщение установлено на {target_time.strftime('%H:%M')}.")
                
                else:
                    await update.message.reply_text("Сначала заполните данные для отправки")
            
            case "Сбросить время отправки":
                if context.user_data['send_hours'] != None and context.user_data['send_minutes'] != None:
                    context.user_data['send_hours'] = None
                    context.user_data['send_minutes'] = None
                    context.user_data['score_time_option'] = 0
                    
                    await update.message.reply_text("Время отправки сброшено")
                
                else:
                    await update.message.reply_text("Вы не заполнили данные до конца")
            
            case _:
                if context.user_data['score_time_option'] == 0:
                    try:
                        number = int(text) 
                        
                        if number >= 0 and number <= 23:
                            context.user_data['send_hours'] = number
                            context.user_data['score_time_option'] += 1
                            await update.message.reply_text("Отлично! Часы отправки зарегистрированы")
                        
                        else:
                            await update.message.reply_text("Число, введенное вами, выходит за рамки временного диапозона часов")
                   
                    except Exception as e:
                        logger.error(f"Не удалось обработать сообщение. {e}")
                        await update.message.reply_text("Не удалось обработать сообщение. Введите число")
                
                elif context.user_data['score_time_option'] == 1:
                    try:
                        number = int(text) 
                        
                        if number >= 0 and number <= 60:
                            context.user_data['send_minutes'] = number
                            context.user_data['score_time_option'] += 1
                            await update.message.reply_text("Отлично! Минуты отправки зарегистрированы")
                       
                        else:
                            await update.message.reply_text("Число, введенное вами, выходит за рамки временного диапозона минут")
                   
                    except Exception as e:
                        logger.error(f"Не удалось обработать сообщение. {e}")
                        await update.message.reply_text("Не удалось обработать сообщение. Введите число")
                
                else:
                    await update.message.reply_text("Вы уже ввели данные для отправки. Переходите к следующему шагу")


# функция отправки списка задач
async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    chat_id = job.chat_id
    tasks_text = job.data
       
    await context.bot.send_message(chat_id=chat_id, text=tasks_text)


# функция остановки отправки списка задач
async def stop_send_daily_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        
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
            job_name = f"daily_reminder_{update.effective_chat.id}"
            current_jobs = context.job_queue.get_jobs_by_name(job_name)
        
            if current_jobs:
                for job in current_jobs:
                    job.schedule_removal()
                await update.message.reply_text("Ежедневое сообщение отключено.")
        
            else:
                await update.message.reply_text("У вас нет запланированной отправки")


