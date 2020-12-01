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
    def __init__(self, id, merchantid, vendor, edition, Price):
        self.id = id
        self.merchantid = merchantid
        self.vendor = vendor
        self.edition = edition
        self.list_prices = []
        self.list_prices.append(Price)
    def toJSON(self):
        return jsonpickle.encode(self) 
    def equals(self, target):
        if (self.id == target.id and 
            self.merchantid == target.merchantid and 
            self.vendor == target.vendor and 
            self.edition == target.edition):
            return True
        else:
            return False

class GamePrices:
    pass
    def __init__(self):
        self.vendorPrices = [] 
        self.counter = 0
    def toJSON(self):
        return jsonpickle.encode(self) 
