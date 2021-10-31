# Файл инициализации бота
from aiogram import Bot
from auth_data import token
from aiogram.dispatcher import Dispatcher

bot = Bot(token=token)
dp = Dispatcher(bot)