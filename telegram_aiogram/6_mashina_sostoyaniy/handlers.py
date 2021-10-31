# Сдесь мы будем использовать хендлеры или функции из других питон файлов
from aiogram.utils import executor
from bot_init import dp
import client
import other
import admin


# async def on_startups( ):
#     print('Бот вышел в онлайн')

#********************************КЛИЕНТСКАЯ ЧАСТЬ********************************#

client.register_handlers_client(dp)

#********************************АДМИНСКАЯ ЧАСТЬ********************************#

admin.register_handlers_admin(dp)

#********************************ДРУГАЯ ЧАСТЬ********************************#

other.register_handlers_other(dp)

# executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
executor.start_polling(dp, skip_updates=True)