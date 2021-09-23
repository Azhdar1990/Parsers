import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import csv

page = 'https://www.compusale.az'
def check_page(page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'
    }
    req = requests.get(page, headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    page_exsist = soup.find('div')
    print('Проверка доступности сайта')
    if req.status_code == 200:
        print('Сайт доступен. Проверка наличия контента.')
    else:
        print('Сайт временно недоступен')
        print('Программа закрывается')
        time.sleep(2)
        exit()
    if page_exsist == None:
        print('На сайте контент не обнаружен')
        print('Программа закрывается')
        time.sleep(2)
        exit()
    else:
        print('ОК!!!')

check_page(page)
