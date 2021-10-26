import requests
import json
import time

start_time = time.time()


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*',
    'accept': 'application/json, text/plain, */*'
}
million = 1000000

def total_page_count():
    #req = requests.get(url=f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/erkek-sneaker-x-g2-c1172?pi={million}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B",headers=headers)
    req = requests.get(url=f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr?wb=44%2C33%2C160%2C159%2C652%2C636%2C803%2C454&wg=2&wc=1172&pi={million}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B",headers=headers)
    response = req.json()
    page_count = response.get("error").split(" ")
    print = page_count[-1]
    #print(f"Total page = {page_count[-1]}")
    return print

#print(total_page_count())
#count = 0
# for i in range (1, int(total_page_count()) + 1):
#     count += 1
#     print(count)

def get_data():
    all_data = []
    true = "True"
    for i in range (1, int(total_page_count()) + 1):
    #for i in range(1, 2):
        request = requests.get(
            url=f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr?wb=44%2C33%2C160%2C159%2C652%2C636%2C803%2C454&wg=2&wc=1172&pi={i}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B",
            headers=headers)
        responce = request.json()
        products = responce.get("result").get("products")

        for b in products:
            stok = str(b.get("inStock"))
            try:
                discountedPriceInfo = (b.get("discountedPriceInfo").split(" ")[1].replace("%", ""))
            except:
                discountedPriceInfo = 0
            if stok == true and int(discountedPriceInfo) >= 40:
                all_data.append({
                    "name": b.get("name"),
                    "selling price": f"{b.get('price').get('sellingPrice')} Tl",
                    "original price": f"{b.get('price').get('originalPrice')} Tl",
                    "discounted Price": f"{b.get('price').get('discountedPrice')} Tl",
                    "url": f"https://www.trendyol.com{b.get('url')}",
                    "discount": f"{discountedPriceInfo} %"
                })
            else:
                continue
#                print(f"Ой {discountedPriceInfo} меньше 40%-тов ((")


        print(f"Запись страницы {i} из {total_page_count()} в json файл")


    with open(f"dump.json", "w", encoding='utf-8-sig') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)


get_data()

finish_time = round(time.time() - start_time)
print(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")

