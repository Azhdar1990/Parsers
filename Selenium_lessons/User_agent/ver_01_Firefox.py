from selenium import webdriver
import random
import time
from fake_useragent import UserAgent

# Качаем веб драйвер Firefox
# https://github.com/mozilla/geckodriver/releases

# Для того что бы узнать какой user-agent используется можно посмотреть на сайте
# http://whatsmyuseragent.org/

# Для  того что бы вставить фэйковый юсер агент воспользуемся библиотекой
# https://pypi.org/project/fake-useragent/

# Список user-agent можно узнать тут
# http://web-data-extractor.net/faq/spisok-aktualnyx-user-agent/

url = "http://whatsmyuseragent.org/"

# Создадим список user-agent - ов
nash_spisok_user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "xxxxxx"
]

# Тут мы создаем опции для нашего селениума.
# Говорим ему что как аргумент будет использоваться user-agent
# Далее варианты.
# Вариант 1 вставляем user-agent из списка который мы создадали в ручную и
# воспользовавшись библиотекой random укажем firefox что бы он брал user-agent из с писка в случайном порядке
# options = webdriver.FirefoxOptions()
# options.set_preference(f"general.useragent.override", random.choice(nash_spisok_user_agent))

# Вариант 2 воспользуемся библиотекой fake-useragent
# Создадим обьект класса useragent
useragent = UserAgent()
# Вариант 2.2 мы можем указывать в ручную user-agent какого браузера использовать
# options = webdriver.FirefoxOptions()
# options.set_preference(f"general.useragent.override", useragent.opera)
# Варимант 2.3 мы можем рандомно используя метод random
# сделать так что бы селениум каждый раз использовал разные user.agent
options = webdriver.FirefoxOptions()
options.set_preference(f"general.useragent.override", useragent.random)

def user_agent_usage(url):

    driver = webdriver.Firefox(
        executable_path="./geckodriver.exe",
        options=options
    )
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        time.sleep(3)
    # В блоке except обрабатывать ошибки если есть
    except Exception as _ex:
        print(_ex)
    # Завершать работу драйвера хром
    finally:
        driver.close()
        driver.quit()



user_agent_usage(url)