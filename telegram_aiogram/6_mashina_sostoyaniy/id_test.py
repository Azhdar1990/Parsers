IDS = []
with open("ids.txt", encoding='utf-8-sig') as r:
    for i in r:
        IDS.append(i.strip())
        print(i.strip())
    print(IDS)
    if "415955184" in IDS:
        print("AVAILABLE")
    else:
        print("NONE")