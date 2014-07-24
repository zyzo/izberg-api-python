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

    def test_newStore(self):
        self.login()

        store = self.api_handler.Store()
        r = random.randint(1,1000)
        store_name = "MonSuperStore%s"%(r)
        store.name = store_name
        store.store_type = "decoration"
        store.application = "/v1/application/10/"
        store.save()
        
        


        #found_store = self.api_handler.Store.search({"pinterest": "pinterestAdress"})








