#!/usr/bin/env python

from requests import get
from my_classes import GamePrices, VendorPrice, Price, BeautifulSoup, datetime, jsonpickle
import getopt, sys
from pprint import pprint
from datetime import datetime

date_format = "%Y-%m-%d %H:%M:%S"

def help_main():
    print("For program help use:\n\t -h or --help\n")
    print("Feed data file use:\n\t-f or --feed\n")
    print("Get prices NOW use:\n\t-n or --now\n")
    print("Get CHEAPEST price ever use:\n\t-c or --cheapest\n")
    print("Get LATEST data feed date use:\n\t-l or --latest-fetch\n")
    print("Get total AMOUNT of feeds use:\n\t-a or --fetch-amounts\n")

def cheapest():
    #print("This is cheapest\n")
    hasOldFile = False
    print('[1] - Loading previous data file....', end="")
    try:
        with open("storeprices.json", "r") as f:
            oldjson =jsonpickle.decode(f.read())
            hasOldFile = True
            print("Finished!")
    except FileNotFoundError:
        print('/!\\ No file found a new one will be created!')
        pass
    except :
        print("json shit KO!")
        pass

    print("[2] - Checking lowest price.....", end="")
    lowestPrice = "ad"
    if hasOldFile:
        lowestPrice = oldjson.vendorPrices[0]
        for s in oldjson.vendorPrices:
            #print("checking: " + s.vendor + " - " + s.edition)
            for p in s.list_prices:
                #print("price: " + p.price + " (" + p.scrapeDate + ")")
                if p.price < lowestPrice.list_prices[0].price:
                    lowestPrice = s
                    lowestPrice.list_prices = []
                    lowestPrice.list_prices.append(p)
    print("Finished!\n")
    print("Lowest price: " + lowestPrice.vendor + " - " + lowestPrice.edition)
    print("Price: " + lowestPrice.list_prices[0].price + " (" + lowestPrice.list_prices[0].scrapeDate + ")")
    #print("Lowest price: "+lowestPrice.vendor)
            
def now():
    print('[1] - Getting url......', end="")
    url = 'https://www.allkeyshop.com/blog/buy-football-manager-2021-cd-key-compare-prices/'
    response = get(url)
    print('Finished!')

    print('[2] - Processing data.....', end="")

    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)

    offers = []
    listOffers = html_soup.find_all("div", class_="offers-table-row")
    for (s) in listOffers:
        strung = s.text
        strung = '|'.join(strung.split()).split("|")
        if strung[-1] == "now":
            offerHref = s.find("a", class_="d-none d-lg-block buy-btn").get("href").split("/")[-1].split("?merchant=")
            array = [strung[0], strung[3], strung[-6], offerHref[0], offerHref[1]]
            offers.append(array)

    games = GamePrices()
    for offer in offers:
        vendorPrice = VendorPrice(offer[3], offer[4], offer[0], offer[1], Price(offer[2]))
        games.vendorPrices.append(vendorPrice)

    print("Finished!\n")
    print(*offers, sep="\n")
    
    text = input("\nFeed data to data file? (s/N)")
    if text == 's' or text == 'S':
        feed()
    else:
        print("Data not feed to file - program will exit now!")

def feed():
    hasOldFile = False
    print('[1] - Loading previous data file....', end="")
    try:
        with open("storeprices.json", "r") as f:
            oldjson =jsonpickle.decode(f.read())
            hasOldFile = True
            print("Finished!")
    except FileNotFoundError:
        print('/!\\ No file found a new one will be created!')
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

    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)

    listOffers = html_soup.find_all("div", class_="offers-table-row")

    offers = []
    for (s) in listOffers:
        strung = s.text
        strung = '|'.join(strung.split()).split("|")
        if strung[-1] == "now":
            offerHref = s.find("a", class_="d-none d-lg-block buy-btn").get("href").split("/")[-1].split("?merchant=")
            array = [strung[0], strung[3], strung[-6], offerHref[0], offerHref[1]]
            offers.append(array)

    games = GamePrices()
    for offer in offers:
        vendorPrice = VendorPrice(offer[3], offer[4], offer[0], offer[1], Price(offer[2]))
        if hasOldFile:
            for (oldP) in oldjson.vendorPrices:
                if vendorPrice.equals(oldP):
                    oldP.list_prices.append(vendorPrice.list_prices[0])
                    break
        games.vendorPrices.append(vendorPrice)

    print("Finished!")
    print("[4] - Writng to data file......", end="")
    games.counter= 0
    if hasOldFile:
        games = oldjson 
        games.counter += 1
        f.close()


    ffinal.write(str(games.toJSON()))
    ffinal.close()
    print("Finished!")

def latest_fetch():
    #print("Latest fetch done")
    #print("This is cheapest\n")
    hasOldFile = False
    print('[1] - Loading previous data file....', end="")
    try:
        with open("storeprices.json", "r") as f:
            oldjson =jsonpickle.decode(f.read())
            hasOldFile = True
            print("Finished!")
    except FileNotFoundError:
        print('/!\\ No file found a new one will be created!')
        pass
    except :
        print("json shit KO!")
        pass

    latestDate = oldjson.vendorPrices[0].list_prices[0].scrapeDate
    for p in oldjson.vendorPrices:
        res = sorted(p.list_prices, key=lambda x: datetime.strptime(x.scrapeDate, date_format), reverse=True)
        if latestDate < res[0].scrapeDate:
            latestDate = res[0].scrapeDate
    
    print("\nLatest data fetch:\t" + latestDate)

def fetch_amount():
    #print("Number of Fetch amount")
    #print("This is cheapest\n")
    hasOldFile = False
    print('[1] - Loading previous data file....', end="")
    try:
        with open("storeprices.json", "r") as f:
            oldjson =jsonpickle.decode(f.read())
            hasOldFile = True
            print("Finished!")
    except FileNotFoundError:
        print('/!\\ No file found a new one will be created!')
        pass
    except :
        print("json shit KO!")
        pass
    if hasOldFile:
        print("\nNumber of fetches:\t" + str(oldjson.counter))


#print("Price of FM21: ", datetime.now().strftime(date_format))

full_cmd_arguments = sys.argv

argument_list = full_cmd_arguments[1:]
short_options = "hcfnla"
long_options = ["help", "cheapest", "feed", "now", "latest-fetch", "fetch-amounts"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print (str(err))
    sys.exit(2)

if len(arguments) == 0:
    print("No arguments passed")

for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        print ("Entering help mode\n")
        help_main()
    if current_argument in ("-c", "--cheapest"):
        print ("Entering check cheapest price mode\n")
        cheapest()
    elif current_argument in ("-f", "--feed"):
        print ("Entering feed mode\n")
        feed()
    elif current_argument in ("-n", "--now"):
        print ("Entering now mode\n")
        now()
    elif current_argument in ("-l", "--latest-fetch"):
        print ("Entering latest fetch mode\n")
        latest_fetch()
    elif current_argument in ("-a", "--fetch-amounts"):
        print ("Entering fetch amount mode\n")
        fetch_amount()
    #elif current_argument in ("-n", "--now"):
    #    print (("Enabling special output mode (%s)") % (current_value))

print("\nEnd Price of FM21: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))