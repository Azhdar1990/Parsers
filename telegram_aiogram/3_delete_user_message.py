from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from auth_data import token
import json
import string

bot = Bot(token=token)
dp = Dispatcher(bot)

# В данном примере в последнем хендлере,
# Бот будет удалять слова которые есть в списке slova.json
#

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


@dp.message_handler()
async def echo_send(message : types.Message):
    # Сдесь мы будем получать все сообщения пользователя message.text
    # Разделять слова пробелами message.text.split(" ") и получаем список из слов которые были отправлены.
    # Проходимся по нему циклом for i in message.text.split(" ") и обрабатываем каждое слово.
    # Приводим его в нижний регистр i.lower()
    # Убераем все маскирующиеся символы translate(str.maketrans("", "", string.punctuation))
    # Библиотека string содержит все символы пунктуации (!,@,# и тд...)
    # метод translate будет удалять символы пунктуации
    # в translate обращаемся к типу данных str и его метод maketrans
    # у maketrans 3 аргумента ("перечень что менять", "перечень на что менять", "указываем символы нужно вообще убрать"
    #
    # Теперь реализуем проверку
    # Далее циклом if смотрим если есть слово в нашем файле и данное слово есть в списке текста полученного от пользователя то удаляем сообщение.
    # метод .intersection (пересечение множеств) позволяет сравнить есть ли совподения или нет.
    # в аргумент intersection поставим наш файл slova.json что бы он сравнивал их с полученными из списка выше.
    # .intersection(set(json.load(open("slova.json"))))
    # если совподений нет то вернется пустой ответ (или пустое множество)
    # поэтому пишем != set()
    # То есть если ответ (мнжество) не пустое значит оно есть в файле slova.json и удаляем сообщение.


    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(" ")}\
        .intersection(set(json.load(open("slova.json", encoding='utf-8-sig')))) != set():
        await message.answer("Ай яй яй... Как не стыдно... 🙁")
        await message.delete()
    #await message.answer("Нет функций для выполнение данной команды 🙁")


# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
executor.start_polling(dp, skip_updates=True)