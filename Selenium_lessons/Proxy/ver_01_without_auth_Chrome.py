from selenium import webdriver
import random
import time
from fake_useragent import UserAgent

# Качаем веб драйвер хрома
# https://chromedriver.storage.googleapis.com/index.html

# Бесплатные прокси можно посмотреть тут
# https://free-proxy-list.net/

# Данный скрипт будет использовать прокси сервер для работы.
# Прокси должен быть без авторизации (бесплатный)

url = "https://2ip.ru"


options = webdriver.ChromeOptions()

# Создадим опцию с прокси (аргументы можно добавлять в селениуме уже к существующим)
options.add_argument("--proxy-server=190.210.211.70:8080")

def user_agent_usage(url):

    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
        options=options
    )
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        time.sleep(5)
    # В блоке except обрабатывать ошибки если есть
    except Exception as _ex:
        print(_ex)
    # Завершать работу драйвера хром
    finally:
        driver.close()
        driver.quit()



user_agent_usage(url)