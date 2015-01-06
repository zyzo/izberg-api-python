# -*- coding: utf-8 -*-
from decimal import Decimal
from helper import IcebergUnitTestCase

class ClientOrder(IcebergUnitTestCase):
    # def test_01_anonymous_add_to_cart(self):
    #     """
    #     Add to cart as anonymous
    #     """
    #     self.login_anonymous()
    #     cart = self.api_handler.Cart()
    #     cart.save()
    #     offer = self.get_random_offer()
        
    #     if hasattr(offer, 'variations') and len(offer.variations) > 0:
    #         for variation in offer.variations:
    #             print variation
    #             print variation.to_JSON()
    #             if variation.stock > 0:
    #                 cart.addVariation(variation, offer)
    #                 break
    #     else:
    #         cart.addOffer(offer)

    #     cart.fetch()

    def test_02_application_user_add_to_cart(self):
        """
        Add to cart as login user
        """
        self.login_user_2()
        cart = self.api_handler.Cart()
        cart.save()
        offer = self.get_random_offer()
        
        if hasattr(offer, 'variations') and len(offer.variations) > 0:
            for variation in offer.variations:
                print variation
                print variation.to_JSON()
                if variation.stock > 0:
                    cart.addVariation(variation, offer)
                    break
        else:
            cart.addOffer(offer)

        cart.fetch()