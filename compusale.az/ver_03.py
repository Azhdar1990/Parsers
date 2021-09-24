import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import csv
import shutil

page = 'https://www.compusale.az'
#URL = 'https://www.compusale.az/index.php?route=product/category&path=103_157'

#print('Здравствуйте.\nДанная программа парсит нужную вам категорию с сайта "compusale.az".\nСобирается следующая информация:\nмодель, цена без НДС, цена с НДС, наличие, ссылка.\nДалее всё сохраняется в exel и открывается сохраненный файл.\nДля начала работы программы вам нужно будет ввести ссылку категории.\nНапример:\nВы зашли в катигорию устойства маршрутизаторы модель unifi.\nhttps://www.compusale.az/index.php?route=product/category&path=85_86_189\nСкопируйте ссылку с браузера и вставьте в программу.')
# Запрашиваем у пользователя ссылку с сайта
URL = input('Введите ссылку с сайта которую будем парсить: ')

# Проверяем доступность сайта  compusale.az если не доступен то заканчиваем работу скрипта
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
        time.sleep(1)
        print('Сайт доступен. Проверка наличия контента.')
    else:
        time.sleep(1)
        print('Сайт временно недоступен')
        print('Программа закрывается')
        time.sleep(2)
        exit()
    if page_exsist == None:
        time.sleep(1)
        print('На сайте контент не обнаружен')
        print('Программа закрывается')
        time.sleep(2)
        exit()
    else:
        time.sleep(1)
        print('Контент найден. Продолжаем...')
###
# Проверяем наличие папок и если нет то создаем новые
def check_folder():
    print('Проверка наличие временных папок')
    if os.path.exists(r'resources'):
        print("...")
    else:
        os.mkdir(r'resources')
    if os.path.exists(r'resources\links'):
        print("...")
    else:
        os.mkdir(r'resources\links')
###

# Создадим функцию которая будет подкл к нашей страници.
# Функция принемает знацение url вставляет его  в библиотеку requests c
# параметрами headers
def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'
    }
# Ниже код которым мы проверяем количество страниц и если страница содержит контент то парсим ее
# Если нет то стоп
# Таким образом мы можем спарсить все страницы в данном линке
# Переменная page пудет увеличиваться на 1 и вставляться в параметры страници
# Далее условие что если на странице ест указанный в супе контент тогда стоп (там указанно что нет сраници)
# или идти дальше
    page = 1
    page_count = []
    for page in range (1, 100000):
        req = requests.get(url + f"&page={page}", headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        page_exsist = soup.find('div', class_='products-filter')
#        print(page_exsist)
        if page_exsist == None:
            print('UPS!! Больше нет данных.')
            print('Всего найдено '+ str(page - 1) + ' cтраниц по указанной ссылке')
            break
        else:
            print('Найдено страниц №: ' + str(page))
            page += 1
    print('Начинаем парсинг')

    all = []
    for item in range(page):
        req = requests.get(url + f"&page={item}", headers)
#        print(req)
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
# Создадим обьект супа со значением src и парсера lxml.
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
        try:
            links = link.find('div', class_='image').find_next('a', class_='product-img').get('href')
        except Exception:
            continue
#        links = link.find('div', class_='image').find_next(class_='product-img has-second-image')
        try:
            model = link.find('div', class_='name').find('a').get_text()
        except Exception:
            continue
#        model = link.find('div', class_='name').find('a').get_text()
        switches_urls[model] = links
#    print(len(switches_urls.keys()))
#        print(model)
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
        print('Парсинг модели №: ' + str(currentLink) + ' из ' + str(len(switches_urls.keys())))

#        print(model + links)

        req = requests.get(links, headers)
        try:
            with open(f'resources/links/{model}.html', 'w', encoding='utf-8-sig') as file:
                file.write(req.text)
        except Exception:
            print('Не получилось собрать инфо о модели № ' + str( currentLink ) + str( model ))
            continue

#        print (req.text)
#        print ('взята ссылка модели: ' + model)
###
#  Далее считываем данные в переменную
#  Открываем каждую сораненную ранее страницу.
        with open (f'resources/links/{model}.html', encoding='utf-8-sig') as file:
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
        with open('final.csv', 'w', newline='', encoding='utf-8-sig') as file:
             writer = csv.writer(file, delimiter=';')
             for row in rows:
                 writer.writerow(row)
             for item in data_list:
                 writer.writerow([item['Model'], item['Price with NDS'], item['Price without NDS'], item['Stok'], item['LINK']])
def open_file():
    print('Парсинг завершен')
    #
    os.startfile(r'final.csv')
    time.sleep(4)


###
# Нужно удалить временные папки.
def del_folders():
    print('Удаляем временные папки')
    if os.path.exists(r'resources\links'):
        shutil.rmtree('resources\links', ignore_errors=True)
    else:
        print("...")
    if os.path.exists(r'resources'):
        shutil.rmtree('resources', ignore_errors=True)
    else:
        print("...")


check_page(page)
check_folder()
get_data(URL)
del_folders()
open_file()