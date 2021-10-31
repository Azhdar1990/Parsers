from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# ReplyKeyboardMarkup этот класс замещает клавиатуру обычную на ту которую мы создаем.
# KeyboardButton   создать каждую кнопу по отдельности. Эти кнопки отправляют то что в них написанно.
# ReplyKeyboardRemove Удаляет клавиатуру


b1 = KeyboardButton("/menu")
b2 = KeyboardButton("/info")
b3 = KeyboardButton("/del_keyboard")
# b4 и b5 отправят инфо не то что в них написанно телеграму. А отправят запросы на контакт и расположение.
b4 = KeyboardButton("Поделиться номером", request_contact=True)
b5 = KeyboardButton("Отправить где я", request_location=True)

# resize_keyboard=True адаптируем клавиатуру под размер экрана устройства
# one_time_keyboard=True прачет клавиатуру после ее использования
#kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

# методом add добавляем наши кнопки в ReplyKeyboardMarkup() c новой строки
#kb_client.add(b1).add(b2)

# методом insert добавляем наши кнопки в ReplyKeyboardMarkup() рядом если есть место.
# kb_client.add(b1).insert(b2)

# методом row добавляем наши кнопки в ReplyKeyboardMarkup() в строку.
#kb_client.row(b1, b2)
kb_client.add(b1).insert(b2).add(b3).row(b4, b5)