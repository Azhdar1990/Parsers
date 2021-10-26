from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from ver_02_asyncio import gather_data
from ver_03_snikers_girl import gather_data_girl
from auth_data import token
import json
import time



# bot = Bot(token="")
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)

# Создаем диспетчер или приветствие + кнопки
@dp.message_handler(commands="start")

async def start(message: types.Message):
    #await message.answer("Hello!")
    start_buttons = ["👟_KİŞİ", "👟_QADIN", "NONE"]
    # что бы кнопки не были больгими укажем (resize_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Trendyol-dan > 20% endirimnən🔥", reply_markup=keyboard)
    await message.answer("Bot-u Maniyev Əjdər yazıb🙎‍♂️", reply_markup=keyboard)

# Создадим условие что если при нажатии на кнопку Крософки
# запускалась функция collect_data() из файла ver_01.py
@dp.message_handler(Text(equals="👟_KİŞİ"))
#start_time = time.time()
async def get_discount_sneakers(message: types.Message):
    await message.answer("Məlumat toplanılır gözləyin 😐")
    await message.answer("+- 1 dəgigə apara bilər 😐")

    await gather_data()


    with open("dump.json", encoding='utf-8-sig') as file:
        data = json.load(file)
    # сдесь мы указываем какие данные будем отображать в телеграме
    # Данные перутся из файла result.json
    for item in data:
        card = f"{hlink(item.get('name'), item.get('url'))}\n" \
               f"{hbold('Model: ')} {item.get('name')}\n" \
               f"{hbold('Faizsız giymət: ')} {item.get('selling price')}\n" \
               f"{hbold('Faiznan giymət: ')} {item.get('discounted Price')}\n" \
               f"{hbold('Faiz: ')} -{item.get('discount')}🔥"
        time.sleep(0.08)
        await message.answer(card)

    # finish_time = round(time.time() - start_time)
    # await message.answer(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")

##########################################################################################

@dp.message_handler(Text(equals="👟_QADIN"))
#start_time_girl = time.time()
async def get_discount_sneakers(message: types.Message):
    await message.answer("Məlumat toplanılır gözləyin 😐")
    await message.answer("+- 1 dəgigə apara bilər 😐")


    await gather_data_girl()


    with open("dump.json", encoding='utf-8-sig') as file:
        data = json.load(file)
    # сдесь мы указываем какие данные будем отображать в телеграме
    # Данные перутся из файла result.json
    for item in data:
        card = f"{hlink(item.get('name'), item.get('url'))}\n" \
               f"{hbold('Model: ')} {item.get('name')}\n" \
               f"{hbold('Faizsız giymət: ')} {item.get('selling price')}\n" \
               f"{hbold('Fariznan giymət: ')} {item.get('discounted Price')}\n" \
               f"{hbold('Faiz: ')} -{item.get('discount')}🔥"
        time.sleep(0.08)
        await message.answer(card)

    # finish_time = round(time.time() - start_time_girl)
    # await message.answer(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")


def bot():
    executor.start_polling(dp)

bot()