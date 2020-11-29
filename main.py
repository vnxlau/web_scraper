#!/usr/bin/python3

from requests import get
from my_classes import GamePrices, VendorPrice, Price, BeautifulSoup, datetime, jsonpickle
    
print("Price of FM21: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
hasOldFile = False
print('[1] - Loading previous data file....', end="")
try:
    with open("storeprices.json", "r") as f:
        oldjson =jsonpickle.decode(f.read())
        hasOldFile = True
        print("Finished!")
except FileNotFoundError as identifier:
    print('/!\ No file found a new one will be created!')
    pass
except :
    print("json shit KO!!")
    pass


print('[2] - Getting url......', end="")
url = 'https://www.allkeyshop.com/blog/buy-football-manager-2021-cd-key-compare-prices/'
response = get(url)
print('Finished!')

print('[3] - Processing data.....', end="")
ffinal = open("storeprices.json", "w")
start_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Price of FM21\n"
#f.write(start_log)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

listOffers = html_soup.find_all("div", class_="offers-table-row")

listNames = html_soup.find_all("span" ,class_="offers-merchant-name")
listPrices = html_soup.find_all("span", class_="price")
listBuyBtn = html_soup.find_all("a", class_="d-none d-lg-block buy-btn")

offers = []
for (s) in listOffers:
    strung = s.text
    strung = '|'.join(strung.split()).split("|")
    #print(strung)
    if strung[-1] == "now":
        offerHref = s.find("a", class_="d-none d-lg-block buy-btn").get("href").split("/")[-1].split("?merchant=")
        #print(offerHref)
        array = [strung[0], strung[3], strung[-6], offerHref[0], offerHref[1]]
        offers.append(array)

#print(*offers, sep="\n")
games = GamePrices()

for offer in offers:
    vendorPrice = VendorPrice(offer[3], offer[4], offer[0], offer[1], Price(offer[2]))
    if hasOldFile:
        for (oldP) in oldjson.vendorPrices:
            if vendorPrice.equals(oldP):
                #print(oldP.vendor)
                oldP.list_prices.append(vendorPrice.list_prices[0])
                break
    games.vendorPrices.append(vendorPrice)

print("Finished!")
print("[4] - Writng to data file......", end="")
if hasOldFile:
    games = oldjson 
    f.close()

ffinal.write(str(games.toJSON()))
print("Finished!")


end_log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "END\n\n"

ffinal.close()