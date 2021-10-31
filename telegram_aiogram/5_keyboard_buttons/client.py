# Файл хендлера "client"
#
from bot_init import bot
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
# импортируем нашу клавиатуру для клиента
from keyboards.keyboards_client import kb_client

# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        # добавим нашу клавиатуру добавив аргумент reply_markup=kb_client
        await bot.send_message(message.from_user.id, "Ты ввел /start или /help", reply_markup=kb_client)
        await bot.send_message(message.from_user.id, "Сработала функция commands_start..")
    except:
        await message.reply("Общение с ботом только через ЛС, напишите ему.")


async def menu(message : types.Message):
    await bot.send_message(message.from_user.id, "Меню пока не готово")

async def info(message : types.Message):
    await bot.send_message(message.from_user.id, "Инфо о нас пока нет")

# reply_markup=ReplyKeyboardRemove() удаляет клавиатуру
async def del_keyboard(message : types.Message):
    await bot.send_message(message.from_user.id, "Удаление клавиатуры", reply_markup=ReplyKeyboardRemove())

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(info, commands=['info'])
    dp.register_message_handler(del_keyboard, commands=['del_keyboard'])