IDS = []
with open("ids.json", encoding='utf-8-sig') as r:
    for i in r:
        print(i.split(":")[1].strip())
        IDS.append(i.split(":")[1].strip())
    print(IDS)
    if "415972116" in IDS:
        print("AVAILABLE")
    else:
        print("NONE")