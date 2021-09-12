import requests
from bs4 import BeautifulSoup

URL = 'https://auto.ria.com/newauto/marka-jaguar/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://auto.ria.com'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


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
            uah_price = 'Цену не указана'
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



#    return cars

## Check get_html function
#def parse():
#    html = get_html(URL)
#    print(html.status_code)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        cars = get_content(html.text)
    else:
        print('Error')

parse()
