# https://www.youtube.com/watch?v=ITELa7JaDm4&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=11

import requests
from bs4 import BeautifulSoup
import os
import csv
import json
import datetime
import time

url = "https://www.labirint.ru/books/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}

# Содадим переменную которая будет иметь значениея времени запуска скрипта
start_time = time.time()


def get_data(url):
    # Переменная будет иметь значение - время запуска скрипта
    start_time = datetime.datetime.now()
    # Создадим переменную которая будет содержать время,число,месяц,год
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    # Создадим csv файл
    with open(f"labirint_{cur_time}.csv", "w", encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название книги",
                "Автор",
                "Издательство",
                "Цена со скидкой",
                "Цена без скидки",
                "Процент скидки",
                "Наличие на складе"
            )
        )
    # Создадим список который будет принимать пропарсенные данные
    books_data = []

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    # Узнаем последнюю страницу сайта
    pages_count = int(soup.find("div", class_="pagination-numbers").find_all("a")[-1].text)
#    print(pages_count)

#     Зная последнюю страницу сайта запустим цикл где добавляя страницу, соберем списки
#     которые содержат нужную нам информацию о книгах и сохраним в переменную books_items
#     под списками имею ввиду тэг tr расположенный в тэге tbody
    for page in range (1, pages_count + 1):
#    for page in range(1, 2):
#        print("hello " + str(page))
        url = f"https://www.labirint.ru/books/?display=table&page={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
#        print(soup)
        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")
#        print(books_items)

#        теперь пройдемся по переменной books_items и соберем нужные нам данные
#        так как все данные в блоке тэга td а мы получаем список то для вывода нужной инфо
#        просто будем указывать номер из списка в квадратных скобках
#        используем метод try exept так как не везде есть информация.
#        каждый результат будем сохранять в отдельную переменную
        for book_info in books_items:
            book_data = book_info.find_all("td")
#            print(book_data)
            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "Нет названия книги"

            try:
                book_author = book_data[1].find("a").text.strip()
            except:
                book_author = "Нет Нет автора"

            try:
#                так как в мы получим 2 текста на разной строке то
#                воспользуясь методом join мы обьединим их в одну строку
                # book_publishing = book_data[2].text
                book_publishing = book_data[2].find_all("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "Нет издательства"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except:
                book_new_price = "Нет нового прайса"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "Нет старого прайса"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "Нет скидки"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "Нет статуса"

#            теперь полученные данные добавим в  заранее созданный список books_data
            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

#            print(book_publishing)
#            При каждом срабатывании данного блока в цикле, дополним (а) csv файл данными из списка
            with open(f"labirint_{cur_time}.csv", "a", encoding='utf-8-sig') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )

#        При каждом срабатывании данного блока в цикле, будем выводить для информативности ниже инфо
        print(f"Обработана {page}/{pages_count}")
        time.sleep(1)

#    Сохраним полученный список books_data в json
    with open(f"labirint_{cur_time}.json", "w", encoding='utf-8-sig') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)

#    создадим переменную которая будет принимать значение времени потраченного на выполнение скрипта

    diff_time = datetime.datetime.now() - start_time
    print("Время выполнения скрипта: " + str(diff_time))

get_data(url)