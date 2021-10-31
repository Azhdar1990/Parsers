import json
with open("dump_girl.json", encoding='utf-8-sig') as file:
    data = json.load(file)
    count = len(data)
    print(count)