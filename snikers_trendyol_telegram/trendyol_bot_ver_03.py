import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
#from telegram_bot_pagination import InlineKeyboardPaginator
from ver_02_asyncio import gather_data
from ver_03_snikers_girl import gather_data_girl
from auth_data import token
import json
import time
import random



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
    await message.answer("Bot 10 mesaj göstərir", reply_markup=keyboard)


# Создадим условие что если при нажатии на кнопку Крософки
# запускалась функция collect_data() из файла ver_01.py
@dp.message_handler(Text(equals="👟_KİŞİ"))
#start_time = time.time()
async def get_discount_sneakers(message: types.Message):
    await message.answer("Məlumat toplanılır gözləyin 😐")
    await message.answer("+- 1 dəqiqə apara bilər 😐")

    await gather_data()


    with open("dump.json", encoding='utf-8-sig') as file:
        data = json.load(file)
        count = len(data)
        # Будем увеличивать на 10 и записывать в файл потом что бы использовать при пагинации.
        for b in range(0, 10):
            with open("numb_kisi.txt", "a", encoding='utf-8-sig') as r:
                r.write(str(b))
        with open("numb_kisi.txt", encoding='utf-8-sig') as r:
            b = (len(r.read()))

        # сдесь мы указываем какие данные будем отображать в телеграме
        # Данные перутся из файла result.json
    try:
        if b <= count:
            for i in range(b, b + 10):
                card = f"{hlink(data[i].get('name'), data[i].get('url'))}\n" \
                       f"{hbold('Model: ')} {data[i].get('name')}\n" \
                       f"{hbold('Faizsız giymət: ')} {data[i].get('selling price')}\n" \
                       f"{hbold('Faiznan giymət: ')} {data[i].get('discounted Price')}\n" \
                       f"{hbold('Faiz: ')} -{data[i].get('discount')}🔥"
                #print(i)
                time.sleep(0.08)
                await message.answer(card)
        #print(count)
            await message.answer("Daha 10 mesaj görmək üçün")
            await message.answer("👟_KİŞİ düyməsini basın")
        else:
            await message.answer("Artıq melumat yoxdur 🙁")
            open('numb_kisi.txt', 'w', encoding='utf-8-sig').close()
    except:
        await message.answer("Yenidən 👟_KİŞİ düyməsini basın")

    # finish_time = round(time.time() - start_time)
    # await message.answer(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")

##########################################################################################

@dp.message_handler(Text(equals="👟_QADIN"))
#start_time_girl = time.time()
async def get_discount_sneakers(message: types.Message):
    await message.answer("Məlumat toplanılır gözləyin 😐")
    await message.answer("+- 1 dəqiqə apara bilər 😐")


    await gather_data_girl()


    with open("dump_girl.json", encoding='utf-8-sig') as file:
        data = json.load(file)
        count = len(data)

# Будем увеличивать на 10 и записывать в файл потом что бы использовать при пагинации.
    for b in range (0, 10):
            with open("numb_qadin.txt", "a", encoding='utf-8-sig') as r:
                r.write(str(b))
    with open("numb_qadin.txt", encoding='utf-8-sig') as r:
        b = (len(r.read()))

    # сдесь мы указываем какие данные будем отображать в телеграме
    # Данные перутся из файла result.json
    try:
        if b <= count:
            for i in range(b, b + 10):
                card = f"{hlink(data[i].get('name'), data[i].get('url'))}\n" \
                       f"{hbold('Model: ')} {data[i].get('name')}\n" \
                       f"{hbold('Faizsız giymət: ')} {data[i].get('selling price')}\n" \
                       f"{hbold('Faiznan giymət: ')} {data[i].get('discounted Price')}\n" \
                       f"{hbold('Faiz: ')} -{data[i].get('discount')}🔥"
                print(i)
                time.sleep(0.08)
                await message.answer(card)

            await message.answer("Daha 10 mesaj görmək üçün")
            await message.answer("👟_QADIN düyməsini basın")
        else:
            await message.answer("Artıq melumat yoxdur 🙁")
            open('numb_qadin.txt', 'w', encoding='utf-8-sig').close()
    except:
        await message.answer("Yenidən 👟_QADIN düyməsini basın")

    # finish_time = round(time.time() - start_time_girl)
    # await message.answer(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")


def bot():
    executor.start_polling(dp, skip_updates=True)

bot()