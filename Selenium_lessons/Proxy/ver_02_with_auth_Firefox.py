# from selenium import webdriver
from seleniumwire import webdriver
import random
import time
from fake_useragent import UserAgent
from proxy_auth_data import login, password

# Качаем веб драйвер хрома
# https://chromedriver.storage.googleapis.com/index.html

# Данный скрипт будет использовать прокси сервер для работы.
# Так же будем использовать авторизацию.Создав для этого отдельный файл питона proxy_auth_data.py
# и импортировав его.
# Мы воспользуемся библиотекой selenium-wire

url = "https://2ip.ru"


options = webdriver.FirefoxOptions()

# создадим словарь proxy-options у которого ключь будет содержать еще один словарь
# который будет подставлять на место логина и пароля переменные указанные в переменных
# таким образом мы авторизируемся на нашем купленном прокси сервере.

proxy_options = {
    "proxy " : {
        "https": f"http://{login}:{password}@190.210.211.70:8080"
    }
}


def user_agent_usage(url):

    driver = webdriver.Firefox(
        executable_path="./geckodriver.exe",
        eleniumwire_options=proxy_options
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