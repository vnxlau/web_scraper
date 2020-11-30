#!/usr/bin/python3

from requests import get
from my_classes import GamePrices, VendorPrice, Price, BeautifulSoup, datetime, jsonpickle
import getopt, sys

def help_main():
    print("This is help\n")

def cheapest():
    print("This is cheapest\n")
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

    lowestPrice = VendorPrice()
    
    if hasOldFile:
        lowestPrice = oldjson.vendorPrices[0]
        for s in oldjson:
            
            

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

    print("Finished!")
    print(*offers, sep="\n")
    
    text = input("Feed data to data file? (s/N)")
    if text == 's' or text == 'S':
        feed()
    else:
        print("Finished!")

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
    if hasOldFile:
        games = oldjson 
        f.close()

    ffinal.write(str(games.toJSON()))
    ffinal.close()
    print("Finished!")

print("Price of FM21: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

full_cmd_arguments = sys.argv

argument_list = full_cmd_arguments[1:]
short_options = "hcfn"
long_options = ["help", "check", "feed", "now"]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print (str(err))
    sys.exit(2)

if len(arguments) == 0:
    print("No arguments passed")

for current_argument, current_value in arguments:
    if current_argument in ("-h", "--help"):
        print ("Displaying help")
        help_main()
    if current_argument in ("-c", "--cheapest"):
        print ("Entering check cheapest price mode")
        cheapest()
    elif current_argument in ("-f", "--feed"):
        print ("Entering feed mode")
        feed()
    elif current_argument in ("-n", "--now"):
        print ("Entering now mode")
        now()
    #elif current_argument in ("-n", "--now"):
    #    print (("Enabling special output mode (%s)") % (current_value))

print("End Price of FM21: ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))