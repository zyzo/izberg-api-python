# -*- coding: utf-8 -*-

# import unittest
# import random

from helper import IcebergUnitTestCase

class ClientTest(IcebergUnitTestCase):
    def test_sso(self):
        self.login()
        self.assertEquals(self.api_handler._sso_response['first_name'], 'Yves')
        self.assertEquals(self.api_handler._sso_response['last_name'], 'Durand')
        self.assertEquals(self.api_handler._sso_response['email'], 'lol@lol.fr')

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

    # def test_newStore(self):
    #     self.login()

    #     store = self.api_handler.Store()
    #     r = random.randint(1, 1000)
    #     store.name = "MonSuperStore%s"%(r)
    #     store.store_type = 3
    #     store.application = "/v1/application/10/"
    #     store.save()

    #     found_store, meta = self.api_handler.Store.search({"name": store.name})
    #     self.assertEquals(found_store[0].store_type, store.store_type)
        



        #found_store = self.api_handler.Store.search({"pinterest": "pinterestAdress"})








