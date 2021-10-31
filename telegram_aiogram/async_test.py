def count():

    for i in range (0, 10):
            with open("numb.txt", "a", encoding='utf-8-sig') as r:
                r.write(str(i))
    with open("numb.txt", encoding='utf-8-sig') as r:
        x = (len(r.read()))
        if x > 150:
            open('numb.txt', 'w', encoding='utf-8-sig').close()
        else:
            print(x)


count()