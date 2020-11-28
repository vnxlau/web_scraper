#!/usr/bin/python3

import jsonpickle
import datetime
from bs4 import BeautifulSoup

# # Classes -----------------------------------------------
# --------------------------
class Price:
    def __init__(self, price):
        self.scrapeDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.price = price
    def toJSON(self):
        return jsonpickle.encode(self) 

class VendorPrice:
    pass
    def __init__(self, vendor, type, Price):
        self.vendor = vendor
        self.type = type
        self.list_prices = []
        self.list_prices = { Price.scrapeDate, Price.price }
    def toJSON(self):
        return jsonpickle.encode(self) 

class GamePrices:
    pass
    def __init__(self):
        self.vendorPrices = [] 
    def toJSON(self):
        return jsonpickle.encode(self) 
