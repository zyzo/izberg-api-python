# -*- coding: utf-8 -*-

import random


class IcebergObjectCreateMixin(object):
    """
    Some shortcuts to create commons objects
    """
    # Create Utils
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


    def create_application(self, namespace = "test-app-lib-python", name = "Test App Lib Python", contact_user = None):
        new_application = self.api_handler.Application()
        new_application.namespace = namespace
        new_application.name = name
        new_application.contact_user = contact_user or self.api_handler.User.me()
        new_application.save()

        return new_application


    def create_merchant(self, name = "test-python-lib-store", application = None):
        # self.assertNotEqual(application, None)

        new_merchant = self.api_handler.Store()
        new_merchant.name = name
        # new_merchant.application = application
        new_merchant.save()

        return new_merchant


    # Get Utils
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

    def get_random_sku(self):
        return "test-sku-%s" % random.randint(0, 1000000000)





