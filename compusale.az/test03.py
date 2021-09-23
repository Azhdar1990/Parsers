import os
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import csv
import shutil

# Запрашиваем у пользователя ссылку с сайта
site = input('Введите ссылку с сайта которую будем парсить: ')
print(site)
