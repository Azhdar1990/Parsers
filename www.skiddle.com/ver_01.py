# https://www.skiddle.com/festivals/search/
# https://www.youtube.com/watch?v=arBTqminwU8&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=6

import os
import requests
from bs4 import BeautifulSoup
import csv
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'
    }
div = 'div'
page = 0
fests_urls_list = []

# Мы знаем что страница прокручевается и в параметрах указывается цыфры с шагом 24
# Создадим цикл и будем записывать значения в переменную page
# Если страница будет содержать тэг DIV то продолжаем если нет то тормозим.
# Таким образом мы получаем количество которое далее будем вводить в следующем цикле
for page in range (24, 10000, 24):
    link = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=30%20Sep%202021&to_date=&maxprice=500&o={page}&bannertitle=April'
    req = requests.get(url=link, headers=headers)
    src = req.text
    if div in src:
        continue
    else:
        break
#print(str(page - 24))
###

# Теперь мы знаем какое число нужно вводить в параметр (мы его получили циклом выше)
# Сохраним ссылки страниц на которых содержаться нужные ссылки
# Далее откроем каждую сохраненную ссылку и соберем ссылки фестивалей сохранив в список fests_urls_list
for i in range(0, page, 24):
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=30%20Sep%202021&to_date=&maxprice=500&o={i}&bannertitle=April'
    req = requests.get(url=url, headers=headers,)
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    with open(f"data/index_{i}.html", "w") as file:
        file.write(html_response)
    with open(f"data/index_{i}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("a", class_="card-details-link")

    for item in cards:
        fest_url = "https://www.skiddle.com" + item.get("href")
        fests_urls_list.append(fest_url)
#print(fests_urls_list)
###

# collect fest info
count = 0
fest_list_result = []
for url in fests_urls_list:
    count += 1
    # print(count)
    # print(url)
    req = requests.get(url=url, headers=headers)
#    print(req)

    try:
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_block = soup.find("div", class_="top-info-cont")

        fest_name = fest_info_block.find("h1").text.strip()
        fest_date = fest_info_block.find("h3").text.strip()
        fest_location_url = "https://www.skiddle.com" + fest_info_block.find("a", class_="tc-white").get("href")
        # get contact details and info
        req = requests.get(url=fest_location_url, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        contact_details = soup.find("h2", string="Venue contact details and info").find_next()
        items = [item.text for item in contact_details.find_all("p")]

        contact_details_dict = {}
        for contact_detail in items:
            contact_detail_list = contact_detail.split(":")

            if len(contact_detail_list) == 3:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip() + ":"\
                                                                       + contact_detail_list[2].strip()
            else:
                contact_details_dict[contact_detail_list[0].strip()] = contact_detail_list[1].strip()

        fest_list_result.append(
            {
                "Fest name": fest_name,
                "Fest date": fest_date,
                "Contacts data": contact_details_dict
            }
        )

    except Exception as ex:
        print(ex)
        print("Damn...There was some error...")

    print('Collecting data...' + str(count))
print('DONE')

with open("fest_list_result.json", "a", encoding="utf-8") as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)