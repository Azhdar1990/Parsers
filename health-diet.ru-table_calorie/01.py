import  requests
import json
from bs4 import BeautifulSoup
import csv

url = 'http://health-diet.ru/table_calorie/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
domain = 'http://health-diet.ru'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
# Проверка функции get_html
html = get_html(url).text
# print (html)



def get_content(html):
   all_categories_dict = {}
   soup = BeautifulSoup(html, 'lxml')
   items = soup.find_all(class_='mzr-tc-group-item-href')

   count = 0

   for item in items:
        item_text = item.text
        item_href = domain + item.get('href')
        all_categories_dict[item_text] = item_href
   with open("all_categories_dict.json", "w") as file:
       json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
   with open("all_categories_dict.json") as file:
       all_categories = json.load(file)
#       print(all_categories)
   iteration_count = int(len(all_categories)) - 1
   print(f"Всего итераций: {iteration_count}")
   for category_name, category_href in all_categories.items():
#       print(category_name)
#       print(category_href)
    #   if count == 0:
            rep = [",", " ", "-", "'"]
            for item in rep:
                if item in category_name:
                    category_name = category_name.replace(item, "_")
    #                print(category_name)
            req = requests.get(url=category_href, headers=HEADERS)
            src = req.text
    #        print(src)

            with open(f"data/{count}_{category_name}.html", "w", encoding='utf-8-sig') as file:
                file.write(src)

            with open(f"data/{count}_{category_name}.html", encoding='utf-8-sig') as file:
                 src = file.read()

            soup = BeautifulSoup(src, "lxml")

            # проверка страницы на наличие таблицы с продуктами
            alert_block = soup.find(class_="uk-alert-danger")
            if alert_block is not None:
                continue

           # собираем заголовки таблицы

            table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    #        print(table_head)
            product = table_head[0].text
            calories = table_head[1].text
            proteins = table_head[2].text
            fats = table_head[3].text
            carbohydrates = table_head[4].text
     #       print(product, calories, proteins, fats, carbohydrates )

            with open(f'parsedCSV/{count}_{category_name}.csv', 'w', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
            # собираем данные продуктов
            products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

            product_info = []
            for item in products_data:
                product_tds = item.find_all("td")

                title = product_tds[0].find("a").text
                calories = product_tds[1].text
                proteins = product_tds[2].text
                fats = product_tds[3].text
                carbohydrates = product_tds[4].text
            #    print(title, calories, proteins, fats, carbohydrates)



            product_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates
                }
            )
            # print(product_info)
            with open(f'parsedCSV/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )

            with open(f"parsedJSON/{count}_{category_name}.json", "a", encoding='utf-8-sig') as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)

            count += 1
            print(f"# Итерация {count}. {category_name} записан...")

            iteration_count = iteration_count - 1

            if iteration_count == 0:
                print("Работа завершена")
                break

            print(f"Осталось итераций: {iteration_count}")
 #           sleep(random.randrange(2, 4))
get_content(html)













#         all_categories_dict.append ({
#             item_text: item_href
#         })
#    return all_categories_dict
   #print(all_categories_dict)

#test = get_content(html)
#print(test)



# def parse (html):
#     rep = [",", " ", "-", "'"]
#     html = get_content(html)
#     print(html[0])
#     category_name = html[0]
#  #   category_href =
#  #   for category_name, category_href in html:
#  #       print(category_name)
#         # for item in rep:
#         #     if item in category_name:
#         #         category_name = category_name.replace(item, "_")
#         # print(category_name)
#
#     print(category_name)

#parse(html)