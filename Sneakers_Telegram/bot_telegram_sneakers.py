from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from ver_01 import collect_data
from auth_data import token
import json

# bot = Bot(token="")
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Создаем диспетчер или приветствие + кнопки
@dp.message_handler(commands="start")
async def start(message: types.Message):
    #await message.answer("Hello!")
    start_buttons = ["Кроссовки", "Телефоны", "Уйгуры"]
    # что бы кнопки не были больгими укажем (resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Товары со скидкой", reply_markup=keyboard)

# Создадим условие что если при нажатии на кнопку Крософки
# запускалась функция collect_data() из файла ver_01.py
@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Идёт сбор данных, подождите...")

    collect_data()

    with open("result.json", encoding='utf-8-sig') as file:
        data = json.load(file)
    # сдесь мы указываем какие данные будем отображать в телеграме
    # Данные перутся из файла result.json
    for item in data:
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
               f"{hbold('Категория: ')} {item.get('category')}\n" \
               f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
               f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_discount')}🔥"

        await message.answer(card)

#Запускаем нашего бота
def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()