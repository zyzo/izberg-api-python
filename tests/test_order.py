# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase

class ClientOrder(IcebergUnitTestCase):
    def test_01_anonymous_add_to_cart(self):
        """
        Add to cart as anonymous
        """
        self.login_anonymous()
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
        

    def test_02_full_order(self, offer_id=None):
        """
        Full order
        """
        self.login()

        cart = self.api_handler.Cart()
        cart.save()
        
        if offer_id:
            offer = self.api_handler.ProductOffer.find(offer_id)
        else:
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

        addresses = self.api_handler.me().addresses()

        if len(addresses)==0:
            address = self.create_user_address()
        else:
            address = addresses[0]

        cart.shipping_address = address

        if cart.has_changed():
            cart.save()

        self.assertEqual(cart.status, "20") # Valide

        order = cart.createOrder()
        order.authorizeOrder()

        self.my_context_dict['order'] = order
        self.my_context_dict['merchant_order'] = order.merchant_orders[0]

    def test_03_confirm_merchant_order(self):
        self.login()
        merchant_order = self.my_context_dict['merchant_order']
        merchant_order.confirm()

            
    def test_04_create_return(self):
        self.login()
        merchant_order = self.my_context_dict['merchant_order']

        return_request = self.api_handler.Return()
        return_request.merchant = merchant_order.merchant
        return_request.order_item = merchant_order.items[0]
        # return_request.comment = u"Test Message With No Special Chars"
        return_request.comment = u"Têst Mèssâge Rétürn Çômmënt"
        return_request.save()
        
        self.my_context_dict['return_request'] = return_request
        
    def test_05_accept_return(self):
        self.login()
        return_request = self.my_context_dict['return_request']
        return_request.accept()
        
        
    def test_06_create_refund(self):
        self.login()
        return_request = self.my_context_dict['return_request']
        merchant_order = self.my_context_dict['merchant_order']
        refund = self.api_handler.Refund()
        refund.return_request = return_request
        refund.merchant_order = merchant_order
        refund.merchant = merchant_order.merchant
        refund.user = self.api_handler.User.me()
        refund.save()






