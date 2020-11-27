#!/usr/bin/python
import datetime

from requests import get
url = 'https://www.allkeyshop.com/blog/buy-football-manager-2021-cd-key-compare-prices/'
response = get(url)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Price of FM21" )

f = open("demofile4.txt", "a")
start_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Price of FM21\n"
f.write(start_log)
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

listnames = html_soup.find_all("div" ,class_="offers-merchant text-truncate")
listprices = html_soup.find_all("span", class_="price")

for (s, p) in zip(listnames, listprices):
    log = s.get('title') + "\t" + p.get('content')+"\n"
    print(log)
    f.write(log)
    
end_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "END\n\n"
f.write(end_log)
f.close()