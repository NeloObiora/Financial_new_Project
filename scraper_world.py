from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

URL = "https://www.worldgovernmentbonds.com/"

#    Scraper-Identity: "Rita-UniProject/ educational scraper

options = Options()
options.add_argument("--headless")  

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.get(URL)
time.sleep(5)                       

doc = BeautifulSoup(driver.page_source, "lxml") 


world_gov = doc.find('tbody')
if world_gov:
    rows = world_gov.find_all('tr')
    print(f"Found {len(rows)} countries")
else:
    print("tbody not found")

countries = []
rating = []
country_yield = []

csv_file = open('world_gov_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Countries', 'Rating', 'Yield'])

for count in rows:
    country_links = count.find_all('a', class_='linkToCountry')
    country = country_links[0].text.strip() if len(country_links) > 0 else 'N/A'
    
    rate = country_links[1].text.strip() if len(country_links) > 1 else 'N/A'
    
    yield_tag = count.find('a', class_='linkT10Y')
    if yield_tag:
        bond_yield = yield_tag.text.strip()
    else:
        yield_td   = count.find('td', class_='w3-right-align w3-bold')
        bond_yield = yield_td.text.strip() if yield_td else 'N/A'

    countries.append(country)
    rating.append(rate)
    country_yield.append(bond_yield)
    
    print(countries[-1])
    print(rating[-1])
    print(country_yield[-1])
    csv_writer.writerow([countries[-1], rating[-1], country_yield[-1]])
      
csv_file.close() 

driver.quit() 








