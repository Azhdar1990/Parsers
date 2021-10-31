 #  Labmda дает возможность поиска какой то фразы в тексте пользователя и если она есть то
#  совершать какое то действие.
#  Так же создадим хендлер который будер реагировать на все те сообщения, хендлра которого нет.
#

from aiogram.utils import executor
from aiogram import Bot, types
from bot_init import dp

@dp.message_handler(commands=["start"])
async def start(message : types.Message):
    await message.reply("Привет ты ввел start")

# Данный хендлер будет искать слово такси в тексте который ввел пользователь.
# Если найдет, то выполнит действие в данном случае выведит текст
# "В твоем тексте есть слово такси."
# @dp.message_handler(lambda message: "такси" in message.text)
# async def taxi(message: types.Message):
#     await message.answer("В твоем тексте есть слово такси.")

# В данном примере бот если увидет что текст пользователя начинаетя с "такси" то
# вернет пользователю текст после слова такси. такси  - 5 символов. Поэтому укажем что
# возвращать с 6-го и далее message.text[6:]

@dp.message_handler(lambda message: message.text.startswith("такси"))
async def terurt_after_taxi_word(message: types.Message):
    await message.answer(message.text[6:])


# Все не найденные команды о которых не занет бот будут попадать в данный хендлер
# на который бот будет реагировать сообщением - "Извини нет такой команды".
#
@dp.message_handler()
async def none(message: types.Message):
    await message.answer("Извини нет такой команды")
    await message.delete()

executor.start_polling(dp, skip_updates=True)