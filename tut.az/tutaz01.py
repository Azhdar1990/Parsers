import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://tut.az/dasinmaz-emlak/ev-alqi-satqisi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://tut.az/'
FILE = 'ev-alqi-satqisi.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# Количество страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='pageNumbers')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
    # Проверяем работу подщета страниц
    # print(pagination)

def get_content(html):
   soup = BeautifulSoup(html, 'html.parser')
   items = soup.find_all('div', class_='products-list_item')
   # Проверяем работу функции get_content
   # print(items)
   emlak = []
   for item in items:
#       uah_price = item.find('span', class_='size16')
#       if uah_price:
#           uah_price = uah_price.get_text().replace(' • ', '')
#       else:
#            uah_price = 'Цена не указана'
       emlak.append({
           'Menzil': item.find('div').find_next(class_='title').get_text(strip=True).replace('...', ''),
           'Elanin Tarixi': item.find('div').find_next(class_='date').get_text().replace('\n', ''),
           'Giymet': item.find('div').find_next('span').get_text().replace('\n', ''),
           'Link': item.find_next('a').get('href'),
       })
   # Проверяем работу функции get_content на начальном этапе
   print (emlak)

#   return emlak

def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Menzil', 'Elanin Tarixi', 'Giymet', 'Link'])
        for item in items:
            writer.writerow([item['Menzil'], item['Elanin Tarixi'], item['Giymet'], item['Link']])


def parse():
#    URL = input('Введите URL: ')
#    URL = URL.strip()
    # Создаем переменную с функцией get_html и где аргумент - наш URL
    html = get_html(URL)
    if html.status_code == 200:
        # Проверяем подключение к сайту print(html.status_code) где ответ должен быть 200 то есть ОК.
        # print(html.status_code)
        # Проверяем работу функции get_content
#        get_content(html.text)
        #Проверяем работу функции pages_count
#        page = get_pages_count(html.text)
#        print(page)
        emlak = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 4):
            print(f'Парсинг страницы {page}')
    #        print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            emlak.extend(get_content(html.text))
 #           print(emlak)
        save_file(emlak, FILE)
        print(f'Получено {len(emlak)} обьявлений(я)')
        os.startfile(FILE)

    else:
        print('Error')

parse()
