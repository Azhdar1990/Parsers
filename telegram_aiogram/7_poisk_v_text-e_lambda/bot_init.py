# Файл инициализации бота
from aiogram import Bot
from auth_data import token
from aiogram.dispatcher import Dispatcher
# Нам надо указать место где бот будет хранить данные.
# В данном примере то оперативная память
# aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# запускаем класс storage
storage = MemoryStorage()

bot = Bot(token=token)
# так же в диспетчер передаем класс хранилища
dp = Dispatcher(bot, storage=storage)
