# -*- coding: utf-8 -*-
import os
import unittest
import random

from icebergsdk.conf import ConfigurationDebug, ConfigurationSandbox #, ConfigurationStage
from icebergsdk.api import IcebergAPI

class IcebergUnitTestCase(unittest.TestCase):
    def setUp(self):
        if os.getenv('DEBUG', False):
            self.api_handler = IcebergAPI(conf = ConfigurationDebug)
        else:
            self.api_handler = IcebergAPI(conf = ConfigurationSandbox)

    def login(self):
        self.api_handler.sso_user(email = "lol@lol.fr", first_name = "Yves", last_name = "Durand")

    def login_user_1(self):
        self.api_handler.sso_user(email = "user1@iceberg-marketplace.com", first_name = "Jeff", last_name = "Strongman")

    def login_user_2(self):
        self.api_handler.sso_user(email = "user2@iceberg-marketplace.com", first_name = "Sara", last_name = "Crôche")

    def direct_login(self):
        self.api_handler.auth_user(username="yvesdurand5269004", email="lol@lol.fr")

    def direct_login_user_1(self):
        self.api_handler.auth_user(username="jeffstrongman", email="user1@iceberg-marketplace.com")

    def direct_login_user_2(self):
        self.api_handler.auth_user(username="saracroche", email="user2@iceberg-marketplace.com")

    def get_random_active_store(self):
        """
        Will return a randow active store with active offers
        """
        # Find a merchant
        stores, meta = self.api_handler.Store.search({'status': "10"})

        max_loop = len(stores)
        store = None
        while max_loop > 0:
            store = random.choice(stores) # Return offer randomly
            max_loop -= 1
            product_offers = store.product_offers()
            if len(product_offers) > 0:
                break

        self.assertNotEqual(store, None)

        return store


    def get_random_offer(self):
        """
        Will return a randow active offer
        """
        stores, meta = self.api_handler.Store.search({'status': "10"})

        test_store = None
        for store in stores:
            product_offers = store.product_offers(params = {'availability': 'in_stock'})
            if len(product_offers) > 0:
                test_store = store
                product_offers = product_offers
                break

        self.assertNotEqual(test_store, None)

        max_loop = len(product_offers)

        while max_loop > 0:
            offer = random.choice(product_offers) # Return offer randomly
            max_loop -= 1
            if offer.stock > 0:
                break

        return offer


    def create_user_address(self):
        user_address = self.api_handler.Address()
        user_address.name = "Test"
        user_address.first_name = self.api_handler.me().first_name
        user_address.last_name = self.api_handler.me().last_name
        user_address.address = "300 rue de charenton"
        # user_address.address2 
        user_address.zipcode = "75012"
        user_address.city = "Paris"
        # user_address.state = 
        user_address.user = self.api_handler.me()
        user_address.country = self.api_handler.Country.search({'code': 'FR'})[0][0]
        # user_address.phone = 
        # user_address.digicode
        # user_address.company
        # user_address.floor
        user_address.save()

        return user_address


