import csv
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_all_pages():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    r = requests.get(url="https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/", headers=headers)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("data/main_page_1.html", "w", encoding='utf-8-sig') as file:
        file.write(r.text)

    with open("data/main_page_1.html", encoding='utf-8-sig') as file:
        src = file.read()
# Открыв html файл внизу мы увидем пагинацию а именно количество страниц.
# Сохраним последнюю цифру что бы потом использовать цикл на ее основе для парсинга ссылок на часы
#
#
    soup = BeautifulSoup(src, "lxml")
    pages_count = soup.find("div", class_="bx-pagination-container").find_all("span")
    page_count = []
    for i in pages_count:
        page_count.append(
            i.text
        )
    last_page = len(page_count)
    # print(last_page)

# Теперь используя номер последней страници, засунем ее в цикл и начнем собирать все страници
# Сохраним каждую страницу
    for i in range(1, last_page + 1):
    #    print("hello " + str(i))
         url = f"https://shop.casio.ru/catalog/g-shock/filter/gender-is-male/apply/?PAGEN_1={i}"
    #
         r = requests.get(url=url, headers=headers)
    #
         with open(f"data/page_{i}.html", "w", encoding='utf-8-sig') as file:
             file.write(r.text)
         print("Find page № "+ str(i))
#         time.sleep(2)

# Укажем питону что бы он отображал дату выполения и куажем ее при сохранении в csv
    cur_date = datetime.now().strftime("%d_%m_%Y")
#    print(cur_date)
    with open(f"data_{cur_date}.csv", "w", encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Артикул",
                "Ссылка",
                "Цена"
            )
        )
# И тах у нас есть переменная last_page которая имеет значение последней страници
# Так же есть html страници с часами.
# Создадим список и будем в него записывать инфо.
# Инфо будем брать из цикла где последняя цифра - значение last_page + 1
# Файлы сохраним в csv и json
#
    data = []
    for page in range(1, last_page + 1):
        print(page)
        with open(f"data/page_{page}.html", encoding='utf-8-sig') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("a", class_="product-item__link")

        for item in items_cards:
            product_article = item.find("p", class_="product-item__articul").text.strip()
            product_price = item.find("p", class_="product-item__price").text.lstrip("руб. ")
            product_url = f'https://shop.casio.ru{item.get("href")}'

            # print(f"Article: {product_article} - Price: {product_price} - URL: {product_url}")

            data.append(
                {
                    "product_article": product_article,
                    "product_url": product_url,
                    "product_price": product_price
                }
            )

            with open(f"data_{cur_date}.csv", "a", encoding='utf-8-sig') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_article,
                        product_url,
                        product_price
                    )
                )

        print(f"[INFO] Обработана страница {page}/5")

    with open(f"data_{cur_date}.json", "a", encoding='utf-8-sig') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



get_all_pages()
