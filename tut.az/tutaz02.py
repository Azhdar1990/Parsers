import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://tut.az/dasinmaz-emlak/ev-alqi-satqisi/3-otaqli-menzil-satilir-elsen-sueleymanov-kuec55-140-m2-101638/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://tut.az/'
FILE = 'ev-alqi-satqisi.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
   soup = BeautifulSoup(html, 'html.parser')
   items = soup.find_all('div', class_='_leftPartContainer _relative')
#   Проверяем работу функции get_content
#   print(items)
   emlak = []
   for item in items:
       emlak.append({
           'Ünvan:': item.find('span', text='Ünvan:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Elanın növü:': item.find('span', text='Elanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Binanın növü:': item.find('span', text='Binanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Rayon:': item.find('span', text='Rayon:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Qəsəbə': item.find('span', text='Qəsəbə:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Elanı yerləşdirən:': item.find('span', text='Elanı yerləşdirən:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Mərtəbə sayı:': item.find('span', text='Mərtəbə sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Mərtəbə:': item.find('span', text='Mərtəbə:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Otaqların sayı:': item.find('span', text='Otaqların sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
           'Sənəd:': item.find('span', text=' Sənəd:').find_next(class_='second_part').get_text().replace('\n', ''),
           'Giymət': item.find('div', class_='price xxl').get_text().replace('\n', ''),
           'Elanın tarixi': item.find('div', class_='flex _flexPart3').find_next(class_='flex').next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.get_text(),
       })
   print(emlak)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
#        print(html.status_code)
#        Проверяем работу функции get_content
        get_content(html.text)
    else:
        print('Error')

parse()