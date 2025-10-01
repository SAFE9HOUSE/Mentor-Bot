import logging
import datetime
import os
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError 
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# прописываем настройку логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# константы 
TOKEN = "----------YOUR_BOT_TOKEN----------" 
TARGET_TIMEZONE = "Europe/Moscow" 

