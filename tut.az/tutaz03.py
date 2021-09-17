import requests
from bs4 import BeautifulSoup
import csv
import os
import json

URL = 'https://tut.az/dasinmaz-emlak/ev-alqi-satqisi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://tut.az/'
FILE = 'ev-alqi-satqisi.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='products-list_item')
#   print (items)
    link = {}
    count = 0
    for item in items:
        blank = item.find('div').find_next(class_='title').get_text(strip=True)
        all_links = item.find('a').get('href')
        link[blank] = all_links
    with open("links/all_links.json", "w", encoding='utf-8-sig') as file:
        json.dump(link, file, indent=4, ensure_ascii=False)
    with open("links/all_links.json", encoding='utf-8-sig') as file:
        all_links = json.load(file)
#            print(all_links)
#        print (blank)
    for category_name, category_href in all_links.items():
#        print(category_href)
#        print(category_name)
# На этом этапе мы получили список ссылок на страницы, сохраненный в формат json
#             rep = [",", " ", "-", "'", "...", ".,", "."]
#             for item in rep:
#                 if item in category_name:
#                     category_name = category_name.replace(item, "_")
#                     print(category_name)
             req = requests.get(url=category_href, headers=HEADERS)
             src = req.text
#             print(src)
# Теперь в переменной src мы получаем каждую страницу
# Далее сохраним каждую ссылку отдельно и потом откроем их по одному для парсинга
             with open(f"links_html/{count}.html", "w", encoding='utf-8-sig') as file:
                 file.write(src)

             with open(f"links_html/{count}.html", encoding='utf-8-sig') as file:
                 src = file.read()

             soup = BeautifulSoup(src, "lxml")
             count += 1


def parse():
     html = get_html(URL)
     if html.status_code == 200:
#         print(html.status_code)
# #        Проверяем работу функции get_content
          get_content(html.text)
     else:
         print('Error')
#
parse()