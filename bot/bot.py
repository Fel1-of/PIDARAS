import os
from aiogram import Bot

API_TOKEN = os.getenv('TOKENPIDARASBOT')
ADMIN_ID = 285942176  # os.getenv('TELEGRAM_ACCESS_ID')

bot = Bot(token=API_TOKEN, parse_mode='html')
