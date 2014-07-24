# -*- coding: utf-8 -*-

import unittest
from icebergsdk.api import IcebergAPI

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.api_handler = IcebergAPI()

    def login(self):
        self.user = self.api_handler.sso("lol@lol.fr", "Yves", "Durand")

    def test_sso(self):
        self.login()
        self.assertEquals(self.user['first_name'], 'Yves')
        self.assertEquals(self.user['last_name'], 'Durand')
        self.assertEquals(self.user['email'], 'lol@lol.fr')

    def test_getCart(self):
        self.login()
        currency = self.api_handler.Cart.mine().currency
        self.assertEquals(currency, 'EUR')

    def test_newCart(self):
        self.login()

        new_cart = self.api_handler.Cart()
        new_cart.save()
        user_cart = self.api_handler.Cart.mine()
        self.assertEquals(user_cart.id, new_cart.id)

    def getProduct():
        self.login()
        
        product = self.api_handler.Product.find(6)
        product_category = product.category
        product.category = 999
        product.save()
        new_product = self.api_handler.Product.find(6)
        self.assertEquals(new_product.id, 999)
        new_product.category = product_category
        new_product.save()







