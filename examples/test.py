# -*- coding: utf-8 -*-

import sys, os, json

import logging
#logging.basicConfig(level=logging.DEBUG)

sys.path[0:0] = [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from icebergsdk.api import IcebergAPI


def logIn():
    api_handler = IcebergAPI()
    #accessToken = os.getenv('ICEBERG_API_PRIVATE_KEY')
    #api_handler = IcebergAPI(access_token=accessToken, username="yvesdurant1032644")
    api_handler.sso("lol@lol.fr", "Yves", "Durand")
    return api_handler

def addOffer():

    api_handler = logIn()
    #Get cart
    user_cart = api_handler.Cart.mine()

    #Find product
    offer = api_handler.ProductOffer.find("52")

    #print propreties of the product you just found
    #print offer.description
    #print offer.price_with_vat
   
    #Add product to cart
    user_cart.addOffer(offer)

    #print total amount of the cart
    print api_handler.Cart.mine().currency
    #print api_handler.Cart.mine().total_amount


def getInfos():

    api_handler = logIn()

    #fetch offer object
    product = api_handler.ProductOffer.find("52")

    print product.to_JSON()
    print product.default_image_url
    print product.description
    for variation in product.variations:
        print "%s items available in size %s, %s euros" %(variation['stock'],variation['name'],variation['price'])

def cartInfos(i):

    api_handler = logIn()

    user_cart = api_handler.Cart.mine()

    print user_cart.shipping_address
    print user_cart.total_amount
    print user_cart.estimated_shipping_country


def userInfos():

    api_handler = logIn()

    me = api_handler.User.me()
    
    #print me.to_JSON()
    print me.username
    print me.first_name
    print me.last_name
    print me.email
    print me.timezone

def storeInfos():

    api_handler = logIn()
    #new_store = api_handler.Store()
    #new_store.name = "Mon store"
    #new_store.save()
    #print new_store.to_JSON()

    store = api_handler.Store.find(11)

    print store.name
    print store.created_on
    print store.long_description
    print store.url

def createStore():

    api_handler = logIn()

    found_store, result = api_handler.Store.search({"store_type": "decoration"})
    #new_store = api_handler.Store()
    #new_store.name = "My store"
    #new_store.application = "/v1/application/10/"
    #new_store.save()

   

def getOrder():

    api_handler = logIn()

    #fetch offer object
    merchant_order = api_handler.MerchantOrder.find(6)

    print merchant_order.amount
    print merchant_order.shipping_address.city
    print merchant_order.shipping_address.country
    print merchant_order.shipping_address.zipcode
    
def getProduct():

    api_handler = logIn()
    #products, meta = api_handler.Product.search({"name__icontains": "Robe"})
    product = api_handler.Product.find(6)
    print product.to_JSON()

    #print meta
    #for product in products:
    #    print product.to_JSON()

def cartInfos(i):

    api_handler = logIn()

    new_cart = api_handler.Cart()
    new_cart.save()

    user_cart = api_handler.Cart.mine()

    new_cart.id == user_cart.id




if __name__ == '__main__':
    #storeInfos("52","lol@lol.fr","Yves","Durand")
    createStore()



