# -*- coding: utf-8 -*-

# import unittest
# import random

from helper import IcebergUnitTestCase

class ClientOrder(IcebergUnitTestCase):
    def test_full_order(self):
        self.login()

        cart = self.api_handler.Cart()
        cart.save()
        
        offer = self.get_random_offer()

        if hasattr(offer, 'variations') and len(offer.variations) > 0:
            for variation in offer.variations:
                if variation.stock > 0:
                    cart.addVariation(variation, offer)
                    break
        else:
            cart.addOffer(offer)

        cart.fetch()

        addresses = self.api_handler.me().addresses()

        if len(addresses)==0:
            # from tests.helper import createUserAddress
            address = self.create_user_address()
        else:
            address = addresses[0]

        cart.shipping_address = address

        if cart.has_changed():
            cart.save()

        print cart.status_localized
        self.assertEqual(cart.status, "20") # Valide

        order = cart.createOrder()
        order.authorizeOrder()



