from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

url = "https://www.zalora.co.id/product-index/#J"
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(f"{url}")
time.sleep(2)  # Allow 2 seconds for the web page to open
page_soup = BeautifulSoup(driver.page_source, "html.parser")
driver.close()

# Get content category
content_soup = page_soup.find_all("div", {"class": "pbl pll prd-index__list"})
print(len(content_soup))

# Scraping category by level
list_category = []
for x in content_soup:
    level1_tag = x.find("div", {"class": "fsxl mbm strong"})
    level1 = level1_tag.text.replace("\n", "").strip()
    print(level1)
    list_category.append(level1)
    level2_tag = x.find_all("a", {"class": "marcas-item"})
    for y in level2_tag:
        y1 = y.text.replace("\n", "").strip()
        print(f";{y1}")
        list_category.append(f";{y1}")

# Write scraped data to a csv file (semicolon separated)
f = open(f"zalora_product_index.csv", "w+", encoding="utf-8")  # open/create file and then append some item (a+)
headers = "Level 1;Level 2\n"
f.write(headers)
for i in range(len(list_category)):
    f.write(f"{list_category[i]}\n")
f.close()
