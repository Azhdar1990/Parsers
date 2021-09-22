import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import csv
URL = 'https://www.compusale.az/index.php?route=product/category&path=85_86_189'

def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'
    }
# Ниже код которым мы проверяем количество страниц и если страница содержит контент то парсим ее
# Если нет то стоп
# Таким обрахом мы можем спарсить все страницы в данном линке
# Переменная page пудет увеличиваться на 1 и вставляться в параметры страници
# Далее условие что если на странице ест указанный в супе контент тогда стоп (там указанно что нет сраници)
# или идти дальше
    page = 1
    page_count = []
    for page in range (1, 100000):
        req = requests.get(url + f"&page={page}", headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        page_exsist = soup.find('div', class_='main-products-wrapper').find('p')
        if page_exsist:
            print('UPS!! Больше нет данных')
            break
        else:
            print('OK!! Добавляем в список')
            # print(page)
            page_count.append(
                page
            )
        page += 1
    print('Распечатка списка: ' + str(page_count))



get_data(URL)
