from selenium import webdriver
import random
import time

# Переключение между вкладками
# Сборка инфо


url = "https://www.avito.ru/rossiya/tovary_dlya_kompyutera/komplektuyuschie/videokarty"

# Создадим список user-agent - ов
nash_spisok_user_agent = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.16"
]


options = webdriver.FirefoxOptions()
options.set_preference(f"general.useragent.override", random.choice(nash_spisok_user_agent))

# отключаем режим webdriver-a
# disable webdriver mode
options.set_preference("dom.webdriver.enabled", False)

options.headless = True


def user_agent_usage(url):

    driver = webdriver.Firefox(
        executable_path="./geckodriver.exe",
        options=options
    )
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        print(driver.window_handles)
        print(f"current URL " + driver.current_url)
        driver.implicitly_wait(10)
        # Собираем в список все iva-item-sliderLink-bJ9Pv и кликнем по первому.
        item = driver.find_elements_by_class_name("iva-item-sliderLink-bJ9Pv")
        item[0].click()
        item[1].click()
        item[2].click()
        driver.implicitly_wait(10)
        # Откроется новая влкадка
        # Все открытые вклади обьединяются в список.
        # То есть 1-ая вкладка в браузере - 0 вторая - 1
        # Проверить это можно распечатав ниже указанную команду
        # driver.window_handles
        print(driver.window_handles)
        # для переключания по вкладках мы можем использовать метод
        # switch_to.window() to куда передадим driver.window_handles[1] указав нужный номер в качестве индекса
        # далее print(f"current URL " + driver.current_url) посмотрим какой URL в данный момент
        driver.switch_to.window(driver.window_handles[1])
        print(f"current URL " + driver.current_url)
        # Выведем имя продавца
        #
        username = driver.find_element_by_class_name("seller-info-name")
        print(f"Имя продавца: {username.text}")
        # Если нужно переключаться на разные вкладки то надо браузер отправить обратно на 0 -ую вкладку
        # то есть на начальную или получим ошибку.
        driver.implicitly_wait(10)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Далее можно открывать другие вкладки
        driver.switch_to.window(driver.window_handles[2])
        print(f"current URL " + driver.current_url)
        username = driver.find_element_by_class_name("seller-info-name")
        on_site = driver.find_elements_by_class_name("seller-info-value")[1]
        print(f"Имя продавца: {username.text}")
        print(f"{on_site.text}")

        driver.implicitly_wait(10)

    # В блоке except обрабатывать ошибки если есть
    except Exception as _ex:
        print(_ex)
    # Завершать работу драйвера хром
    finally:
        driver.close()
        driver.quit()



user_agent_usage(url)