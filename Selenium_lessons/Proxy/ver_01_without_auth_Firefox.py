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


options = webdriver.FirefoxOptions()

# Создадим опцию с прокси
proxy = "190.210.211.70:8080"
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities["marionette"] = True
firefox_capabilities["proxy"] = {
    "proxyType": "MANUAL",
    "httpProxy": proxy,
    "sslProxy": proxy
}

def user_agent_usage(url):

    driver = webdriver.Firefox(
        executable_path="./geckodriver.exe",
        proxy=proxy
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