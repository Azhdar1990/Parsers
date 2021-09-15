import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'http://172.16.60.10/logdata?format=txt'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

data = []
def parse():
    html = get_html(URL)
    with open(f"text/text.txt", "w", encoding='utf-8-sig') as file:
        file.write(html.text)
    src = open(f"text/text.txt", mode='r', encoding='utf-8-sig')
    for line in src:
        data.append({
            line.replace('\n', '')
        })
        print(line.strip())
#    print(data[-6:])

parse()

