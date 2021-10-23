import requests
from datetime import datetime
import telebot
from auth_data import token

#  pip3 install wheel telebot pytelegrambotapi
# Создадим функцию для сбора стоимости btc
# Сохраним в json Далее посмотрев полученный результат в http://jsonviewer.stack.hu/
# Создадим переменную которая будет иметь стоимость btc
def get_data():
    req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
    response = req.json()
    print(response)
    sell_price = response["btc_usd"]["sell"]
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")

# Создадим бота аргумент который будет присваивать значения нашего токена из
# файла auth_data.py
def telegram_bot(token):
    bot = telebot.TeleBot(token)
# Далее создадим текст приветсвия когда юсер зайдет на бота нашего
    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Hello friend! Write the 'price' to find out the cost of BTC!")
# Далее будем ждать какой текст введет пользователь
# Если это будет price тогда выведем функцию get_data() или вставим код сюда.
# Если текст не price тогда выведем сообщение
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text.lower() == "price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
                response = req.json()
                sell_price = response["btc_usd"]["sell"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn...Something was wrong..."
                )
        else:
            bot.send_message(message.chat.id, "Whaaat??? Check the command dude!")
# Ниже указанным значением мы делаем возможным работу нашего бота
# иначе скрипт при запуске сразу же закроется
    bot.polling()


#get_data()
telegram_bot(token)