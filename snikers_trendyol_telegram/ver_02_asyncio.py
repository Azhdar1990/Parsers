import requests
import json
import asyncio
import aiohttp
import time

start_time = time.time()


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*',
    'accept': 'application/json, text/plain, */*'
}
million = 1000000

all_data = []
true = "True"

def total_page_count():
    #req = requests.get(url=f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/erkek-sneaker-x-g2-c1172?pi={million}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B",headers=headers)
    req = requests.get(
        url=f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr?wb=44%2C33%2C160%2C159%2C652%2C636%2C803%2C454&wg=2&wc=1172&pi={million}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B",
        headers=headers)
    response = req.json()
    page_count = response.get("error").split(" ")
    print = page_count[-1]
    #print(f"Total page = {page_count[-1]}")
    return print


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        all_data = []
        true = "True"
        #for page in range(1, 50):
        for page in range(1, int(total_page_count()) + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_page_data(session, page):
    #url = f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/erkek-sneaker-x-g2-c1172?pi={page}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B"
    url = f"https://public.trendyol.com/discovery-web-searchgw-service/v2/api/infinite-scroll/sr?wb=44%2C33%2C160%2C159%2C652%2C636%2C803%2C454&wg=2&wc=1172&pi={page}&storefrontId=1&culture=tr-TR&userGenderId=1&pId=aumZRaKGJ2&scoringAlgorithmId=2&categoryRelevancyEnabled=false&isLegalRequirementConfirmed=false&searchStrategyType=DEFAULT&productStampType=TypeA&searchTestTypeAbValue=B"
    async with session.get(url=url, headers=headers) as response:
        res = await response.json()
        products = res.get("result").get("products")

        for b in products:
            stok = str(b.get("inStock"))
            try:
                TL = b.get("discountedPriceInfo").split(" ")
            except:
                continue

            try:
                discountedPriceInfo = (b.get("discountedPriceInfo").split(" ")[1].replace("%", ""))
            except:
                discountedPriceInfo = 0

            #if stok == true and int(discountedPriceInfo) >= 40 and "TL" not in TL:
            if stok == true and int(discountedPriceInfo) >= 20 and "TL" not in TL:
                all_data.append({
                    "name": b.get("imageAlt"),
                    "selling price": f"{b.get('price').get('sellingPrice')} Tl",
                    "original price": f"{b.get('price').get('originalPrice')} Tl",
                    "discounted Price": f"{b.get('price').get('discountedPrice')} Tl",
                    "url": f"https://www.trendyol.com{b.get('url')}",
                    "discount": f"{discountedPriceInfo} %"
                })
            else:
                continue
            # if "TL" in TL:
            #     print("contain TL")
            # else:
            #     print("no TL found")
#                print(f"Ой {discountedPriceInfo} меньше 40%-тов ((")


        #print(f"Запись страницы {page} из {total_page_count()} в json файл")

    with open(f"dump.json", "w", encoding='utf-8-sig') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)

def main():
    asyncio.get_event_loop().run_until_complete(gather_data())

    with open(f"dump.json", "w", encoding='utf-8-sig') as file:
        json.dump(all_data, file, indent=4, ensure_ascii=False)

#main()

# finish_time = round(time.time() - start_time)
# print(f"Затраченное на работу скрипта время: {finish_time} секунд(ы)")

