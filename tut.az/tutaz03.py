import requests
from bs4 import BeautifulSoup
import csv
import os
import json

URL = 'https://tut.az/dasinmaz-emlak/ev-alqi-satqisi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
HOST = 'https://tut.az/'
FILE = 'result/result.csv'



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
             linkss = soup.find_all('html')
             itemss = soup.find_all('div', class_='_leftPartContainer _relative')
            #   Проверяем работу функции get_content
            #   print(items)
             emlak = []
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
# Создадим списом с нужными нам значениями.
                 emlak.append({
                      'Unvan:': item.find('span', text='Ünvan:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Elanın növü:': item.find('span', text='Elanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Binanın növü:': item.find('span', text='Binanın növü:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Qəsəbə': alert_Qəsəbə,
                      'Rayon:': alert_Rayon,
                      'Elanı yerləşdirən:': item.find('span', text='Elanı yerləşdirən:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Mərtəbə sayı:': item.find('span', text='Mərtəbə sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Mərtəbə:': item.find('span', text='Mərtəbə:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Otaqların sayı:': item.find('span', text='Otaqların sayı:').find_next(class_='second_part').get_text().replace('\xa0', ''),
                      'Sənəd:': item.find('span', text=' Sənəd:').find_next(class_='second_part').get_text().replace('\n', ''),
                      'Giymət:': item.find('div', class_='price xxl').get_text().replace('\n', ''),
                 })
             for item in linkss:
                 emlak.append ({
                     'address': item.find('link', rel='canonical').get('href')
                 })

             # with open(f'result/result.csv', 'w', newline='', encoding='utf-8-sig') as file:
             #     writer = csv.writer(file, delimiter=';')
             #     writer.writerow(['Ünvan', 'Elanın növü', 'Binanın növü', 'Qəsəbə', 'Rayon', 'Elanı yerləşdirən', 'Mərtəbə sayı', 'Mərtəbə', 'Otaqların sayı', 'Sənəd', 'Giymət'])
             #     for item in emlak:
             #         writer.writerow([item['Unvan:']])
             print(emlak)
#             return emlak
             count += 1

# def save_file(items, path):
#     with open(path, 'w', newline='', encoding='utf-8-sig') as file:
#         writer = csv.writer(file, delimiter=';')
#         writer.writerow(['Ünvan', 'Elanın növü', 'Binanın növü', 'Qəsəbə', 'Rayon', 'Elanı yerləşdirən', 'Mərtəbə sayı', 'Mərtəbə', 'Otaqların sayı', 'Sənəd', 'Giymət'])
#         for item in items:
#             writer.writerow([item['Unvan:'], item['Elanın növü:']], )

def parse():
     html = get_html(URL)
     if html.status_code == 200:
#         print(html.status_code)
# #        Проверяем работу функции get_content
#           emlak = []
#           emlak.extend(get_content(html.text))
#           print(emlak)
#           save_file(emlak, FILE)
           get_content(html.text)

     else:
         print('Error')
#
parse()