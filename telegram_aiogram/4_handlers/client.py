# Файл хендлера "client"
#
from bot_init import bot
from aiogram import types, Dispatcher


# @dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Ты ввел /start или /help")
        await bot.send_message(message.from_user.id, "Сработала функция commands_start..")
    except:
        await message.reply("Общение с ботом только через ЛС, напишите ему.")



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])