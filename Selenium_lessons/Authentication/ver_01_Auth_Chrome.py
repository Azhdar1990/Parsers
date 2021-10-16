from selenium import webdriver
import random
import time
from auth_data import login, password
from selenium.webdriver.common.keys import Keys

# Данный скрипт будет проходить аудентификацию на сайте


url = "https://vk.com/"

nash_spisok_user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.16"
]
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random.choice(nash_spisok_user_agent)}")


def user_agent_usage(url):

    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
        options=options
    )
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        time.sleep(1)
        # создадим переменную email_input
        # запросим метод find_element_by_id и найдем id index_email
        # index_email - указан в поле ввода email
        # что бы ввести наш email указанный в файле auth_data.py
        # импортируем его.
        # Далее используем метод clear() что бы заранее очистить поле ввода
        # Далее используя метод send_keys укажем переменную
        # login. Таким образом мы вводим наш email
        # таким же способом введем и пароль
        email_input = driver.find_element_by_id("index_email")
        email_input.clear()
        email_input.send_keys(login)

        pass_input = driver.find_element_by_id("index_pass")
        pass_input.clear()
        pass_input.send_keys(password)
        # Далее мы имитируем нажатие кнопки "Войти"
        # Вариант 1 найдем id index_login_button и методом click() кликнем на нее
        #login_button = driver.find_element_by_id("index_login_button").click()
        # time.sleep(5)
        # Вариант 2 имитация нажатия кнопки ENTER
        # для этого надо импортировать ключи
        # from selenium.webdriver.common.keys import Keys
        # вызываем метод send.keys, указываем обьект Keys,
        # затем обьекту Keys говорим нажать ENTER
        # У данной библиотеки много других имитаций помимо ENTER
        pass_input.send_keys(Keys.ENTER)
        time.sleep(1)
        # Далее для наглядности откроем вкладку Друзья в открывшимся окне
        # найдем id l_fr эта кнопка "Друзья" и кликнем на нее
        login_button = driver.find_element_by_class_name("fl_r").click() # закроем вкладку предупреждения
        time.sleep(1)
        login_button = driver.find_element_by_id("l_fr").click()
        time.sleep(5)

    # В блоке except обрабатывать ошибки если есть
    except Exception as _ex:
        print(_ex)
    # Завершать работу драйвера хром
    finally:
        driver.close()
        driver.quit()

user_agent_usage(url)

