import json
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://dawaai.pk/brands/chughtai-labs-576'

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    print("Scrolling...")


soup = BeautifulSoup(driver.page_source, 'html.parser')
card_bodies = soup.find_all("div", {"class": "card-body"})

d = {'Chugtai Labs': []}

count = 0
for div in card_bodies:
    try:
        test = {'name': div.find('h2').text.strip()}
    except Exception as e:
        print(f"{e}")
        continue
    prices = re.findall(r'\d+', div.find('h4').text.strip().replace(',', ''))
    if len(prices) == 2:
        test['actual_price'] = prices[1]
        test['discount_price'] = prices[0]
    else:
        test['discount_price'] = 'N/A'
        test['actual_price'] = prices[0]

    d["Chugtai Labs"].append(test)

    count += 1

print(json.dumps(d, indent=2))
