import requests
from bs4 import BeautifulSoup
import csv
import os
import json

URL = 'https://tut.az/dasinmaz-emlak/ev-alqi-satqisi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://tut.az/'
FILE = 'result.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='products-list_item')
#   print (items)
    link = {}
    count = 0
    emlak = []
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
             linkss = soup.find_all('html')
             itemss = soup.find_all('div', class_='_leftPartContainer _relative')
            #   Проверяем работу функции get_content
            #   print(items)

             for item in itemss:
# Не везде указывают Qəsəbə. Создадим условие что если не указано то написать qeyd olunmayib.
                 alert_Qəsəbə = item.find('span', text='Qəsəbə:')
                 if alert_Qəsəbə:
                     alert_Qəsəbə = alert_Qəsəbə.find_next(class_='second_part').get_text().replace('\xa0', '')
                 else:
                     alert_Qəsəbə = "geyd olunmayib"
# Создадим списом с нужными нам значениями.
# Не везде указывают Rayon. Создадим условие что если не указано то написать qeyd olunmayib.
                 alert_Rayon = item.find('span', text='Rayon:')
                 if alert_Rayon:
                     alert_Rayon = alert_Rayon.find_next(class_='second_part').get_text().replace('\xa0', ''),
                 else:
                     alert_Rayon = "geyd olunmayib"
             for item in linkss:
                 linkas = item.find('link', rel='canonical').get('href')
# Создадим списом с нужными нам значениями.
                 emlak.append({
                      'Unvan:': item.find('span', text='Ünvan:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Elanın növü:': item.find('span', text='Elanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Binanın növü:': item.find('span', text='Binanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Qəsəbə:': alert_Qəsəbə,
                      'Rayon:': alert_Rayon,
                      'Elanı yerləşdirən:': item.find('span', text='Elanı yerləşdirən:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Mərtəbə sayı:': item.find('span', text='Mərtəbə sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Mərtəbə:': item.find('span', text='Mərtəbə:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Otaqların sayı:': item.find('span', text='Otaqların sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Sənəd:': item.find('span', text=' Sənəd:').find_next(class_='second_part').get_text().replace('\n', ''),
                      'Giymət:': item.find('div', class_='price xxl').get_text().replace('\n', ''),
                      'LINK:': linkas,
                 })
#             print(emlak)
#             return emlak
             count += 1
             rows = zip(['Unvan'],['Elanın növü'],['Binanın növü'], ['Qəsəbə:'], ['Rayon:'], ['Elanı yerləşdirən:'], ['Mərtəbə sayı:'], ['Mərtəbə:'], ['Otaqların sayı:'], ['Sənəd:'], ['Giymət:'], ['LINK:'])
             with open('result/result.csv', 'w', newline='', encoding='utf-8-sig') as file:
                 writer = csv.writer(file)
                 for row in rows:
                     writer.writerow(row)
                 for item in emlak:
                     writer.writerow([item['Unvan:'], item['Elanın növü:'], item['Binanın növü:'], item['Qəsəbə:'], item['Rayon:'], item['Elanı yerləşdirən:'], item['Mərtəbə sayı:'], item['Mərtəbə:'], item['Otaqların sayı:'], item['Sənəd:'], item['Giymət:'], item['LINK:'], ])
             print('Парсинг обьявления № '+ str(count))

def parse():
     html = get_html(URL)
     if html.status_code == 200:
           get_content(html.text)
           os.startfile(r'result\result.csv')
     else:
         print('Error')
parse()