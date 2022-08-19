import json

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import json


url = 'https://dawaai.pk/brands/chughtai-labs-576'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
mydivs = soup.find_all("div", {"class": "card-body"})

d = {}
for div in mydivs:
    lab_name = div.find('a', {"class": "product-brand-name"}).text.strip()
    if lab_name in d:
        test = {'name': div.find('a', {"class": "get-values"}).text.strip()}
        prices = re.findall(r'\d+', div.find('h4').text.strip().replace(',', ''))
        if len(prices) == 2:
            test['actual_price'] = prices[1]
            test['discount_price'] = prices[0]
        else:
            test['discount_price'] = 'N/A'
            test['actual_price'] = prices[0]

        d[lab_name].append(test)
    else:
        print("Dic Initialized")
        d[lab_name] = []


print(json.dumps(d, indent=2))
