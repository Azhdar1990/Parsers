import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from urllib.parse import unquote
import random
import json
#Качаем веб драйвер хрома
#https://chromedriver.storage.googleapis.com/index.html
#

url = "https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}
# get_source_html Будем получать исходный код страници
def get_source_html(url):
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe"
    )

    driver.maximize_window()
# В блоке try мы будем творить магию
    try:
        # Вызываем метод get и отправляем наш браузер на страницу
        # Поставим задержку что бы страница успела прогрузиться time.sleep(3)
        driver.get(url=url)
        time.sleep(3)

        while True:
            # Ищем класс catalog-button-showMore

            find_more_element = driver.find_element_by_class_name("catalog-button-showMore")
            # Если он содержит дочерний класс hasmore-text
            # Завершаем работу чикла и сохранем html
            if driver.find_elements_by_class_name("hasmore-text"):
                with open("source-page.html", "w", encoding='utf-8-sig') as file:
                    file.write(driver.page_source)
                break
            # Иначе используя actions.move_to_element перейдем опять на catalog-button-showMore
            # и будем подгружать страницу.
            # Мы как бы имитируем прокрутку страници вниз и дойдя до hasmore-text а это
            # указывает что страница последняя, мы сохраняем получанный html
            # спим 3 сек что бы страница успела подгрузиться
            else:
                actions = ActionChains(driver)
                actions.move_to_element(find_more_element).perform()
                time.sleep(3)

# В блоке except обрабатывать ошибки если есть
    except Exception as _ex:
        print(_ex)
# Завершать работу драйвера хром
    finally:
        driver.close()
        driver.quit()

# Получив полный список карточек соберем ссылки на каждую карточку
# Что бы потом пробижавшись по ним собрать нужную нам инфо
def get_items_urls(file_path):
    with open(file_path, encoding='utf-8-sig') as file:
        src = file.read()
    #print(src)
    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="minicard-item__container")
    #print(items_divs)

    urls = []
    for item in items_divs:
        item_url = item.find("div", class_="minicard-item__rating").get("data-js-lnk")
        urls.append(item_url)
    #print(urls)

    with open("items_urls2.txt", "w", encoding='utf-8-sig') as file:
        for url in urls:
            file.write(f"{url}\n")

    print("[INFO] Urls collected successfully!")
#
# Далее пробижимся по ссылка и соберем нужную информацию
#
def get_data(file_path):
    with open(file_path, encoding='utf-8-sig') as file:
        # urls_list = file.readlines()

        # Первым делом прочитаем файл и сохраним все ссылки обратно в список
        # Первый вариант убрать /n в списке
        # clear_urls_list = []
        # for url in urls_list:
        #     url = url.strip()
        #     clear_urls_list.append(url)
        # print(clear_urls_list)
        # Второй вариант убрать /n в списке используя ist compihation
        urls_list = [url.strip() for url in file.readlines()]
        # print(urls_list)
    result_list = []
    # Ниже переменная которая имеет значение - количество ссылок в файле
    urls_count = len(urls_list)
    count = 1
    # Создаем цикл где будем отправлять запрос на каждый url
    #for url in urls_list:
    for url in urls_list[:1]: # Воспользуемся срезом что бы пропарсить первую ссылку и проверить скрипт
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        try:
            item_name = soup.find("span", {"itemprop": "name"}).text.strip()
        except Exception as _ex:
            item_name = None

        item_phones_list = []
        try:
            item_phones = soup.find("div", class_="service-phones-list").find_all("a", class_="js-phone-number")
        # Телефонов может быть несколько поэтому засуним в цикл
        # Так как мы получим href в виде tel:121234124
        # То разобьем : - ем на 2 значения tel и номер и заберем значение -1
        # Таким образом получим номер
            for phone in item_phones:
                item_phone = phone.get("href").split(":")[-1].strip()
                item_phones_list.append(item_phone)
        except Exception as _ex:
            item_phones_list = None

        try:
            item_address = soup.find("address", class_="iblock").text.strip()
        except Exception as _ex:
            item_address = None
        # На сайте может быть несколько указанных сайтов и наз могут по разному
        # Мы с помущя моу=дуля re в которой можем вставить поиск по шаблонам, укажем шаблон и если нашел
        # то далее найдем ссылку
        # Шаблон - Сайт|Официальный сайт
        try:
            item_site = soup.find(text=re.compile("Сайт|Официальный сайт")).find_next().text.strip()
        except Exception as _ex:
            item_site = None
        #
        #
        #
        social_networks_list = []
        try:
            item_social_networks = soup.find(text=re.compile("Страница в соцсетях")).find_next().find_all("a")
            for sn in item_social_networks:
                sn_url = sn.get("href")
                # Так как на сайте ссылки на соц сети не чистые а с редиректом
                # то мы должны обрезать ненужное.
                # Воспользуемся модулем unqoute из библиотеки urllib
                # test.py покажет как выгладет ссылка
                # И того ссылка находется между "?to=" и "&"
                # Обрежим и получим ссылку
                sn_url = unquote(sn_url.split("?to=")[1].split("&")[0])
                social_networks_list.append(sn_url)
        except Exception as _ex:
            social_networks_list = None
        # Забьем полученное в список result_list
        #
        #
        result_list.append(
            {
                "item_name": item_name,
                "item_url": url,
                "item_phones_list": item_phones_list,
                "item_address": item_address,
                "item_site": item_site,
                "social_networks_list": social_networks_list
            }
        )

        time.sleep(random.randrange(2, 5))

        if count % 10 == 0:
            time.sleep(random.randrange(5, 9))

        print(f"[+] Processed: {count}/{urls_count}")

        count += 1

    with open("result.json", "w", encoding='utf-8-sig') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)

    print("[INFO] Data collected successfully!")

#get_source_html(url)
#get_items_urls(file_path="./source-page.html")
get_data(file_path="./items_urls2.txt")