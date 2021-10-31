# Файл хендлера "other"
#
from aiogram import types, Dispatcher
import json, string

#@dp.message_handler()
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open("slova.json", encoding='utf-8-sig')))) != set():
        await message.answer("Ай яй яй... Как не стыдно... 🙁")
        await message.delete()
    else:
        await message.answer("Нет функций для выполнение данной команды 🙁")


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)