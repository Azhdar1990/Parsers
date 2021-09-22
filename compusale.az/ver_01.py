import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import csv
URL = 'https://www.compusale.az/index.php?route=product/category&path=85_86_189'

# Создадим функцию которая будет подкл к нашей страници.
# Функция принемает знацение url вставляет его  в библиотеку requests c
# параметрами headers
def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'
    }

    all = []
    for item in range(1, 4):
        req = requests.get(url + f"&page={item}", headers)
        all.append({
            req.text
        })
    aalo = str(all)
# Сохраним вывод в файл.
    with open(f'resources/main_page.html', 'w', encoding='utf-8-sig') as file:
        file.write(aalo)
#        print (aalo)
###
# Откроем полученный файл
    with open(f'resources/main_page.html', encoding='utf-8-sig') as file:
        src = file.read()
#        print (src)
###
# Создадим обьект супа со знацением src и парсера lxml.
# То есть начнем парсить страницу.
    soup = BeautifulSoup(src, 'lxml')
# Получим блок с данными (ссылки и тд) и сохраним в переменную switch_urls
# Соберем ссылки и название моделей из switch_urls
# Для этого пробежимся по циклу links который будет принимать значения переменной switch_urls
# Загрузим данные в словарь switches_urls  где ключь - название коммутатора, значение - ссылка
# Создадим словарь switches_urls  где ключь - название коммутатора, значение - ссылка
    switches_urls = {}
    models = {}
    switch_urls = soup.find_all('div', class_='product-thumb')
    for link in switch_urls:
        links = link.find('a', class_='product-img has-second-image').get('href'.strip())
        model = link.find('div', class_='name').find('a').get_text()
        switches_urls[model] = links
#        print(switches_urls)
###
# Далее надо пройтись по каждой ссылке и собрать нужную нам инфо for model, links in switches_urls.items():
# Сначало методом get будем пробигаться по ссылкам.
# Сохраним каждую ссылку с ее данными в отдельный файл
# Присвоим каждой ссылке название из ключа нашего словаря switches_urls
# Создадим переменную currentLink и будем записывать туда номер пропарсенной страницы
# Создадим переменную totalLink и запишем общее количество страниц
# Далее создадим цикл for base, dirs, files in os.walk(r'resources\links'):
# где будем подщитаем общее количество страниц и запишем в переменную totalLinks
# Далее в цикле for model, links in switches_urls.items():
# переменной currentLinks ,будем присваивать по 1 при каждом парсинге страници
# В этом же цикле будем печатать номер конкретной страници и общее количество
# Создадим список для будующих данный которые будем парсить
    data_list = []
###
    currentLink = 0
    totalLinks = 0
    for base, dirs, files in os.walk(r'resources\links'):
        for lin in files:
            totalLinks += 1

    for model, links in switches_urls.items():
        currentLink += 1
        print('Парсинг модели №: ' + str(currentLink) + ' из ' + str(totalLinks))
#        print(model + links)

        req = requests.get(links, headers)
        with open(f'resources/links/{model}.html', 'w', encoding='utf-8-sig') as file:
            file.write(req.text)
#        print (req.text)
#        print ('взята ссылка модели: ' + model)
###
#  Далее считываем данные в переменную
#  Открываем каждую сораненную ранее страницу.
        with open (f'resources/links/{model}.html') as file:
            src = file.read()
#            print(src)
###
# Создаем обьект супа который будет парсить данные из переменной src
# Начинаем собирать нужные данные
        soup = BeautifulSoup(src, 'lxml')
        model = soup.find('ul', class_='list-unstyled').find_next('li', class_='product-model').find('span').get_text()
        price_NDS = soup.find('div', class_='product-price').get_text()
        price_NO_NDS = soup.find('div', class_='product-tax').get_text()
# Ниже я указал 2 варианта парсинга с условиями для переменной stok.
# Если есть то присвоить переменной.
# Если нет то вывести сообщение 'No INdofration'
# Первый способ используя if  else
#          stok_info = stok = soup.find('div', class_='product-stats').find_next('li', class_='product-stock in-stock')
#
#          # if stok_info:
#          #     stok = stok_info.find('span').get_text()
#          # else:
#          #     stok = 'No information'
###
# Второй способ используя try except Exception
        try:
            stok = soup.find('div', class_='product-stats').find_next('li', class_='product-stock in-stock').find(
                'span').get_text()
        except Exception:
            stok = "Məlumat yoxdur"
###
        link = links
#        print(stok)
###
#
# Теперь добавим в вышесозданный список полученные данные
        data_list.append({
            'Model': model,
            'Price with NDS':price_NDS ,
            'Price without NDS':price_NO_NDS,
            'Stok': stok,
            'LINK':link,
        })
#        print(data_list)
# # Теперь сохраним полученную информацию в csv
# # Создадим переменную rows которая будет хранить название столцов
# # Потом создадим цикл где будем записывать каждый столбец из переменной rows в файл csv
# # Потом дальше из нашего списка data_list будем записывать данные каждый в отдельный столбец
        rows = zip(['Model'], ['Price with NDS'], ['Price without NDS'], ['Stok'], ['LINK'])
        with open('final/final.csv', 'w', newline='', encoding='utf-8-sig') as file:
             writer = csv.writer(file, delimiter=';')
             for row in rows:
                 writer.writerow(row)
             for item in data_list:
                 writer.writerow([item['Model'], item['Price with NDS'], item['Price without NDS'], item['Stok'], item['LINK']])


#
    print('Парсинг завершен')
#
    os.startfile(r'final\final.csv')

###

get_data(URL)

