from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from auth_data import token


bot = Bot(token=token)
dp = Dispatcher(bot)

# При запуске бота будет срабатывать данная функция
# Её нужно передать в executor для запуска
# В данном примере кода бот будет в онлайн, он напишет приветсвие к командную строку.
# async def on_startup():
#     print("я онлайн")

#********************************КЛИЕНТСКАЯ ЧАСТЬ********************************#
# Укажем команды на какие бот бует реагировать.
# Если пользователь напишет  /start или /help то сработает данная функция.
@dp.message_handler(commands=['start', 'help'])
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Ты ввел /start или /help")
        await bot.send_message(message.from_user.id, "Сработала функция commands_start..")
    except:
        await message.reply("Общение с ботом только через ЛС, напишите ему.")

@dp.message_handler(commands=['ты'])
async def hwo_i_am(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Я бот написанный человеком по имени Аждар Маниев")
    except:
        await message.reply("Общение с ботом только через ЛС, напишите ему.")




@dp.message_handler()
async def echo_send(message : types.Message):
    await message.answer("Нет функций для выполнение данной команды 🙁")
#********************************АДМИНСКАЯ ЧАСТЬ********************************#

#********************************ОБЩАЯ ЧАСТЬ********************************#

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
executor.start_polling(dp, skip_updates=True)