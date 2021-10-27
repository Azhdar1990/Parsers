# Конвертируем файл в json
#
import json


ar = []


with open("slova.txt", encoding='utf-8-sig') as r:
    for i in r:
        # разделяем все в файле где в качестве разделителя у нас строка (\n)
        # мы получаем списко где будет слово потом пустота.
        # возьмем только первый индекс в каждом списке [0]
        n = i.lower().split('\n')[0]
        # print(n)
        # ar.append(n)
        # Далее пишем условие что если в полученном значении нет пустоты то добавляем в список.
        if n != "":
            ar.append(n)
    print(ar)
    # сохраняем в json
with open("slova.json", "w", encoding='utf-8-sig') as e:
    json.dump(ar, e)

with open("4_Hendlers/slova.json", "w", encoding='utf-8-sig') as e:
    json.dump(ar, e)