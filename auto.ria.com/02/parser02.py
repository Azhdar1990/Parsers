import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-jaguar/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# Количество страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
#Проверить пагинацию
#    print (pagination)


# Сам парсер
def get_content(html):
   soup = BeautifulSoup(html, 'html.parser')
   items = soup.find_all('section', class_='proposition')
 #   print(items)

   cars = []
   for item in items:
       uah_price = item.find('span', class_='size16')
       if uah_price:
           uah_price = uah_price.get_text().replace(' • ', '')
       else:
            uah_price = 'Цена не указана'
       cars.append({
           'Модель': item.find('div', class_='proposition_title').get_text(strip=True),
           'Ссылка': HOST + item.find('a', class_='proposition_link').get('href'),
           'Цена в долларах': item.find('span', class_='green').get_text(strip=True),
           'Цена в Гривнях': uah_price,
           'Город': item.find('span', class_='item region').get_text(strip=True),
   #        'city': item.find('svg', class_='svg_i16_pin').find_next('span').get_text(),

       })
#   Для проверки парсера
#   print(cars)
   return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена в $', 'Цена в UAH', 'Город'])
        for item in items:
            writer.writerow([item['Модель'], item['Ссылка'], item['Цена в долларах'], item['Цена в Гривнях'], item['Город']])


## Check get_html function
#def parse():
#    html = get_html(URL)
#    print(html.status_code)

def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} актомобилей(я)')
        os.startfile(FILE)
#        print(cars)
#        print(len(cars))
    else:
        print('Error')

parse()
