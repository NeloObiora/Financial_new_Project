import requests
from bs4 import BeautifulSoup
import time
from datetime import date
import re
import csv

URL = "https://www.cnbc.com/finance/"

Headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "X-Scraper-Identity": "Rita-UniProject/ educational scraper",
    "Accept": "application/rss+xml, application/xml, text/xml",
}
time.sleep(3)

months = {
    'January':'01', 'February':'02', 'March':'03', 'April':'04',
    'May':'05', 'June':'06', 'July':'07', 'August':'08',
    'September':'09', 'October':'10', 'November':'11', 'December':'12'
}

def clean_date(date_text):
    if "ago" in date_text.lower():
        return str(date.today())
    match = re.search(r'([A-Za-z]+)\s(\d+)\w+\s(\d{4})', date_text)

    if match:
        month_name = match.group(1)  
        day  = match.group(2)  
        year = match.group(3)  

        month_num  = months[month_name]
        day_padded = day.zfill(2)
        return f"{year}-{month_num}-{day_padded}"
    return date_text

response = requests.get(URL, headers= Headers)
#print(f"Status code:{response.status_code}")
doc = BeautifulSoup(response.text, "lxml")

headline = []
link = []
data = []

cnbc_news = doc.find_all("div", class_ ="Card-textContent")

csv_file = open('cnbc_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline', 'Date', 'Link'])

for card in cnbc_news:
    title = card.find('a', class_='Card-title')
    datetime_= card.find('span', class_="Card-time")
    

    if title and datetime_:
        headline.append(title.text.strip())
        data.append(clean_date(datetime_.text.strip()))
        link.append(title['href'])
    
        print(headline[-1])
        print(data[-1])
        print(link[-1])
        
        csv_writer.writerow([headline[-1], data[-1], link[-1]])
      
csv_file.close() 

