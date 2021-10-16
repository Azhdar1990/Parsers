from selenium import webdriver
import random
import time
from auth_data import login, password
from selenium.webdriver.common.keys import Keys

# Отключаем флаг что скрипт  - робот
# Для проверки используем ссылку
#


url = "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"

nash_spisok_user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.16"
]
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random.choice(nash_spisok_user_agent)}")

# отключаем режим webdriver-a
# # for older ChromeDriver under version 79.0.3945.16
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")


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

