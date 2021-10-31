from bot_init import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
# from keyboards.keyboards_client import kb_client
# Импортируем все что нужно для использования нашей админки в режиме (Машины состояния)
# Будем указывать в handler-ах  что данный handler используется конкретно в Машине состояний.
from aiogram.dispatcher import FSMContext
# Импортируем 2 класса State, StatesGroup
from aiogram.dispatcher.filters.state import State, StatesGroup
# Импортируем импорт текста
from aiogram.dispatcher.filters import Text

# создадим пласс наших состояний
# дадим любое название в нашем случаем FSMadmin
# класс будет состоять из 4 -ех пунктов последовательных вопросов.
# Запишем в этот класс наши состояния. В данном случае их 4.
# 1 Отправка фото. 2 Название. 3 Описание. 4 Цена.
# каждой переменной мы дали класс состояния State . Грубо говоря что бы бот сохранял все то что юсер введет.
class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


ID = None
# Создадим список с IDS которые смогут работать с админкой.
# Данный список будет брать значения из файла ids.json где хранятся ID-ки.
IDS = []

# Ниже хендлер уместен если бот в группе какой то где сидят многие.
# Он там проверит если человек который пишет ему является админом группы тогда допускаем в админку.
# # @dp.message_handler(commands=["moderator"], is_chat_admin=True)
# async def make_changes_command(message: types.Message):
#     global ID
#     ID = message.from_user.id
#     await bot.send_message(message.from_user.id, "Привет админ")#, reply_markup=button_case_admin)
#     await message.delete()


# Теперь напишем базовый хендлер который запускает нашу машину состояний.
# Начало диалога загрузки нового пункта меню.
# Сначало проверим есть ли ID пользователя который нам пишет в json документе где храним все İD кто
# может работать с админкой.
# Данный handler старта. то есть он не находится в режиме состояний state=None
# await FSMadmin.photo.set() запускаем наш класс и переменную photo и говорим боту что бы он сохранил ответ
# пользователя .set(). Далее пишем что нужно сделать пользователю.
# И того как только админ напишет Загрузить боту, бот перейдет в режим машины состояний

#@dp.message_handler(commands="Загрузить", state=None)
async def cm_start(message: types.Message):
    with open("ids.json", encoding='utf-8-sig') as r:
        for i in r:
            IDS.append(i.split(":")[1].strip())
    #if message.from_user.id == ID:
    if str(message.from_user.id) in IDS:
        await FSMadmin.photo.set()
        await message.reply("Загрузи фото")
        #print(IDS)
        IDS.clear()
    else:
        await message.reply("Извини но ты не админ 😒")
        #print(IDS)
        IDS.clear()
    #await message.reply(message.from_user.id)

# В любой машине состояния Должна быть кнопа отмены если юсер передумал создавать.
# Нужно что бы была возможность пользователю выйти из машины состояния самому.
# state="*" в каком бы из состояний не находился бот, если он введет (отмена),бот выйдет з режима состояния.
# current_state = await state.get_state() проверяем в каком состоянии сейчас бот.
# if current_state is None если бот не в каком состоянии тогда возвращаем NONE.
# В другом случаее если он в каком либо состоянии, бот выходит из режима состояния.

#@dp.message_handler(state="*", commands="отмена")
#@dp.message_handler(Text(equals="отмена", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Вы вышли. Ваши данные не сохранены.")

# Далее пишем handler который будет ловить ответ на "Загрузи фото" от пользователя.
# state=FSMadmin.photo так бот понимает что именно в нижний хентдлеп попадет ответ от юсера
#     async with state.proxy() as data:
#         data['photo'] = message.photo[0].file_id
# Эта часть кода записывает в словарь data фото но не целиком а присвевает ему ID
# Бот отправляя картинку будет отправлять по ID
# Далее переключаем наш класс дальше await FSMadmin.next() и говорим юсеру что делать дальше
# await message.reply("Введи название")

#@dp.message_handler(content_types=["photo"], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply("Введи название")

# Далее ловим ответ на "Введи название"
# Синтаксис данного handler-а почти такой же что и у выше написанного handler-а
# Разница в типе сохраниения текста data['name'] = message.text
# Далее следующий вопрос "Введи описание"

#@dp.message_handler(state=FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMadmin.next()
    await message.reply("Введи описание")

# Далее ловим ответ на "Введи описание"
#
#
#
#@dp.message_handler(state=FSMadmin.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMadmin.next()
    await message.reply("Введи цену")
#
#
# data['price'] = float(message.text) так как это цена то переведем ее в число с плавующей точкой.
# В данном handler-е так как он последний мы останавливаем машину состояния и выводим бот-а из него.
# После выхода из данного состояния, бот удаляет все то что юсер записал.
# Что бы сохранить, надо ввести :
# Вариант 1:
# async with state.proxy() as data:
#   await message.reply(str(data))
# Вариант 2:
# Указать функцию которая будет записывать все в базу данных
# async with state.proxy() as data:
#   await message.reply(str(data))
# sql_add(state)
#
# до  await state.finish()
#
#@dp.message_handler(state=FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.reply("Данные сохранены")
    await state.finish()

# теперь надо импортировать это все в основной файл
# для этого создадим функцию как у client.py
#
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands="Загрузить", state=None)
    dp.register_message_handler(cancel_handler, state="*", commands="отмена")
    dp.register_message_handler(cancel_handler, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=["photo"], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    #dp.register_message_handler(make_changes_command, commands=["moderator"], is_chat_admin=True)