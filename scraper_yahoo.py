import requests
from bs4 import BeautifulSoup
import csv
import time
import re

URL = "https://finance.yahoo.com/markets/stocks/most-active/"

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "X-Scraper-Identity": "Rita-UniProject/ educational scraper",
    "Accept": "application/rss+xml, application/xml, text/xml",
}
time.sleep(3)

response = requests.get(URL, headers= Headers)
print(f"Status code:{response.status_code}")
doc = BeautifulSoup(response.text, "lxml")

stock = []
pct_change = []
stock_price = []

csv_file = open('yahoo_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Stock_Name', 'Stock_Price', 'Percentage_Change'])

yahoo_rows = doc.find_all('tr', attrs={'data-testid': 'data-table-v2-row'})
for rows in yahoo_rows:
    name = rows.find('div', class_="leftAlignHeader companyName yf-362rys enableMaxWidth")
    pct_cell = rows.find('td', attrs={'data-testid-cell': 'percentchange'})
    price_cell = rows.find('td', attrs={'data-testid-cell': 'intradayprice'})
    
    if name and pct_cell and price_cell:
        stock_name = name['title']
        percentage_chge = pct_cell.find('span', attrs={"data-testid":"colorChange"}).text.strip()
        price = price_cell.find('span', attrs={"data-testid":"change"}).text.strip()
        
    
        stock.append(stock_name)
        pct_change.append(percentage_chge)
        stock_price.append(price)
        
        print(stock[-1])
        print(stock_price[-1])
        print(pct_change[-1])
        

        csv_writer.writerow([stock[-1], stock_price[-1], pct_change[-1]])
      
csv_file.close() 



