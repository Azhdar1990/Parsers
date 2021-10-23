import requests
from datetime import datetime
import telebot
import json

#  pip3 install wheel telebot pytelegrambotapi
# https://www.youtube.com/watch?v=rEMNf1wmyJ8&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=16

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'bx-ajax': 'true'
}

url = "https://salomon.ru/catalog/muzhchiny/obuv/"

url_json = "https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-11.5%20uk/apply/"


def get_page_html(url):
    request = requests.get(url=url, headers=headers)
    with open(f'main_page.html', 'w', encoding='utf-8-sig') as file:
        file.write(request.text)


def get_page_json(url):
    request = requests.get(url=url, headers=headers)
    with open(f"dump.json", "w", encoding='utf-8-sig') as file:
        json.dump(request.json(), file, indent=4, ensure_ascii=False)


def collect_data():
    request = requests.get(url="https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-11.5%20uk/apply/", headers=headers)
    data = request.json()
    # getting page count
    page_count = data.get("pagination").get("pageCount")
    #print(page_count)

    result_dada = []
    items_urls = []
    #get data from each page
    for i in range(1, page_count + 1):
        url = f"https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-11.5%20uk/apply/?PAGEN_1={i}"
        responce = requests.get(url=url,headers=headers)
        data = responce.json()

        # parse each sneakers on eache page
        products = data.get("products")
        for product in products:
            #here we are finding sneakers info
            #we will parce sneakers with discount only
            #in json file there is colors block witch has price block witch has discount info
            # if discount will not = 0 then we will get info
            product_colors = product.get("colors")
            for b in product_colors:
                discount = b.get("price").get("discountPercent")
                #print(discount)
                # Так как есть дубликаты товаров на страницах то создав список items_urls
                # Мы будем его пополнять ссылками товаров
                # Если ссылка b.get("link") не будет найдена в items_urls то сбор данных продолжится
                if discount != 0 and b.get("link") not in items_urls:
                    items_urls.append(b.get("link"))
                    result_dada.append(
                        {
                            'title': b.get("title"),
                            "category": b.get("category"),
                            "link": f"https://salomon.ru{b.get('link')}",
                            "price_base": b.get("price").get("base"),
                            "price_discount": b.get("price").get("sale"),
                            "discount_percent": b.get("price").get("discountPercent")
                        }
                    )
        print(f"Парсинг страницы: {i} из {page_count}")
    #Now save all info
    with open(f"result.json", "w", encoding='utf-8-sig') as file:
        json.dump(result_dada, file, indent=4, ensure_ascii=False)


#get_page_html(url)
#get_page_json(url_json)
collect_data()