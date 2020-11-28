#!/usr/bin/python3

from requests import get
from my_classes import GamePrices, VendorPrice, Price, BeautifulSoup, datetime, jsonpickle

print("load just written")
with open("storeprices.json", "r") as f:
    oldjson =jsonpickle.decode(f.read())
    print(oldjson.vendorPrices[0].vendor)

url = 'https://www.allkeyshop.com/blog/buy-football-manager-2021-cd-key-compare-prices/'
response = get(url)

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " Price of FM21" )

ffinal = open("storeprices.json", "w")
start_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Price of FM21\n"
#f.write(start_log)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

listnames = html_soup.find_all("div" ,class_="offers-merchant text-truncate")
listprices = html_soup.find_all("span", class_="price")

games = GamePrices()
for (s, p) in zip(listnames, listprices):
    name = s.get('title')
    gamePrice = p.get('content')
    a = VendorPrice( name, "edition", Price(gamePrice))
    #f.write(str(a)
    #print(a.toJSON())
    games.vendorPrices.append(a)

ffinal.write(str(games.toJSON()))

end_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "END\n\n"
#f.write(end_log)
ffinal.close()



