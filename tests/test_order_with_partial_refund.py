# -*- coding: utf-8 -*-
from decimal import Decimal
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
        

    def full_order(self, offer_ids=None, number_of_offers=3):
        """
        Full order
        """
        self.login()

        cart = self.api_handler.Cart()
        cart.save()
        
        offers = []
        
        if offer_ids:
            for offer_id in offer_ids:
                offers.append(self.api_handler.ProductOffer.find(offer_id))
        else:

            for i in xrange(number_of_offers):
                offers.append(self.get_random_offer())
            

        for offer in offers:
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

    def test_02_full_order(self):
        """
        Full order
        """
        self.full_order()

    def test_03_confirm_merchant_order(self):
        """
        Confirm merchant order
        """
        self.login()
        merchant_order = self.my_context_dict['merchant_order']
        merchant_order.confirm()

            
    def test_04_create_return(self):
        """
        Create Return
        """
        self.login()
        merchant_order = self.my_context_dict['merchant_order']
        return_requests = []
        items_to_return = merchant_order.items[:-1] ## we return everything except 1 item (partial refund)
        order_item_not_refunded = merchant_order.items[-1]
        for order_item in items_to_return:
            return_request = self.api_handler.Return()
            return_request.merchant = merchant_order.merchant
            return_request.order_item = order_item
            return_request.reason = 6
            return_request.return_type = 2
            # return_request.comment = u"Test Message With No Special Chars"
            return_request.comment = u"Têst Mèssâge Rétürn Çômmënt"
            return_request.save()
            return_requests.append(return_request)
        
        self.my_context_dict['return_requests'] = return_requests
        self.my_context_dict['order_item_not_refunded'] = order_item_not_refunded
        
    def test_05_accept_return(self):
        """
        Accept Return Requests
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        for return_request in return_requests:
            return_request.accept()
        
        
    def test_06_create_partial_refund(self):
        """
        Create Partial Refund
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        merchant_order = self.my_context_dict['merchant_order']
        refund = self.api_handler.Refund()
        refund.return_requests = return_requests
        refund.merchant_order = merchant_order
        refund.merchant = merchant_order.merchant
        refund.user = self.api_handler.User.me()
        refund.partial_refund = True
        refund.shipping = merchant_order.shipping_vat_included
        refund.adjustment = 0
        refund.memo = u"Mémô"
        refund.seller_note = u"Séllèr Nötè" 
        refund.sync = True
        refund.save()
        self.my_context_dict['refund'] = refund

        theoretical_amount = sum([Decimal(return_request.order_item.amount_vat_included) for return_request in return_requests])
        self.assertEqual(Decimal(refund.amount), theoretical_amount)

        self.assertEqual(refund.status, "complete")


    def test_07_check_transactions(self):
        """
        Check First Partial Refund Transactions
        """
        self.direct_login_iceberg_staff()

        order = self.my_context_dict['order']
        refund = self.my_context_dict['refund']
        order_item_not_refunded = self.my_context_dict['order_item_not_refunded']


        refund_transaction = self.api_handler.Transaction.findWhere({"order":order.id, "transaction_type":2})

        app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(app_transactions), 1)
        app_refund_transaction = app_transactions[0]

        merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(merchant_transactions), 1)
        merchant_refund_transaction = merchant_transactions[0]

        mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":refund_transaction.id})[0]
        ## if we find some mp_transactions, there should be revenue sharing # TODO make a call to know if revenue sharing
        has_revenue_sharing = len(mp_transactions) > 0 
        if has_revenue_sharing:
            self.assertEqual(len(mp_transactions), 1)
            mp_refund_transaction = mp_transactions[0]

        transaction_sum = Decimal(app_refund_transaction.amount) + Decimal(merchant_refund_transaction.amount)
        if has_revenue_sharing:
            transaction_sum += Decimal(mp_refund_transaction.amount)
        transaction_sum = - transaction_sum

        total_refund_amount = Decimal(refund.total_refund_amount)

        self.assertEqual(total_refund_amount, transaction_sum)

        theoretical_refund_amount = Decimal(order.amount_vat_included) - Decimal(order_item_not_refunded.amount_vat_included)

        # self.assertEqual(total_refund_amount, theoretical_refund_amount)
        amount_diff = abs(abs(total_refund_amount) - abs(theoretical_refund_amount))
        self.assertTrue(amount_diff <= Decimal("0.01"))


        ## This was the checks for Full Refund : TODO do other checks ?

        # sell_transaction = self.api_handler.Transaction.findWhere({"order":order.id, "transaction_type":1})
        # app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":sell_transaction.id})[0]
        # self.assertEqual(len(app_transactions), 1)
        # app_sell_transaction = app_transactions[0]
        # merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":sell_transaction.id})[0]
        # self.assertEqual(len(merchant_transactions), 1)
        # merchant_sell_transaction = merchant_transactions[0]
        # mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":sell_transaction.id})[0]
        # self.assertEqual(len(mp_transactions), 1)
        # mp_sell_transaction = mp_transactions[0]
        # self.assertEqual(Decimal(merchant_sell_transaction.amount), -Decimal(merchant_refund_transaction.amount))
        # self.assertEqual(Decimal(app_sell_transaction.amount), -Decimal(app_refund_transaction.amount))
        # self.assertEqual(Decimal(mp_sell_transaction.amount), -Decimal(mp_refund_transaction.amount))






    def test_08_create_return(self):
        """
        Create another Return to refund the last item
        """
        self.login()
        merchant_order = self.my_context_dict['merchant_order']
        return_requests = []
        return_request = self.api_handler.Return()
        return_request.merchant = merchant_order.merchant
        return_request.order_item = self.my_context_dict['order_item_not_refunded']
        return_request.reason = 6
        return_request.return_type = 2
        # return_request.comment = u"Test Message With No Special Chars"
        return_request.comment = u"Têst Mèssâge Rétürn Çômmënt"
        return_request.save()
        return_requests.append(return_request)
        
        self.my_context_dict['return_requests'] = return_requests
        
    def test_09_accept_return(self):
        """
        Accept the other Return Requests
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        for return_request in return_requests:
            return_request.accept()
        
        
    def test_10_create_partial_refund(self):
        """
        Create Partial Refund
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        merchant_order = self.my_context_dict['merchant_order']
        refund = self.api_handler.Refund()
        refund.return_requests = return_requests
        refund.merchant_order = merchant_order
        refund.merchant = merchant_order.merchant
        refund.user = self.api_handler.User.me()
        refund.partial_refund = True
        refund.shipping = 0
        refund.adjustment = 0
        refund.memo = u"Mémô"
        refund.seller_note = u"Séllèr Nötè" 
        refund.sync = True
        refund.save()
        self.my_context_dict['refund'] = refund

        theoretical_amount = sum([Decimal(return_request.order_item.amount_vat_included) for return_request in return_requests])
        self.assertEqual(Decimal(refund.amount), theoretical_amount)

        self.assertEqual(refund.status, "complete")


    def test_11_check_transactions(self):
        """
        Check Second Partial Refund Transactions
        """
        self.direct_login_iceberg_staff()

        order = self.my_context_dict['order']
        refund = self.my_context_dict['refund']
        order_item_not_refunded = self.my_context_dict['order_item_not_refunded']


        refund_transactions = self.api_handler.Transaction.search({"order":order.id, "transaction_type":2})[0]
        self.assertEqual(len(refund_transactions), 2)

        refund_transaction = refund_transactions[0] ## ordered by -timestamp so should be the first one

        app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(app_transactions), 1)
        app_refund_transaction = app_transactions[0]

        merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(merchant_transactions), 1)
        merchant_refund_transaction = merchant_transactions[0]

        mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":refund_transaction.id})[0]
        ## if we find some mp_transactions, there should be revenue sharing # TODO make a call to know if revenue sharing
        has_revenue_sharing = len(mp_transactions) > 0 
        if has_revenue_sharing:
            self.assertEqual(len(mp_transactions), 1)
            mp_refund_transaction = mp_transactions[0]

        transaction_sum = Decimal(app_refund_transaction.amount) + Decimal(merchant_refund_transaction.amount)
        if has_revenue_sharing:
            transaction_sum += Decimal(mp_refund_transaction.amount)
        transaction_sum = - transaction_sum


        total_refund_amount = Decimal(refund.total_refund_amount)

        self.assertEqual(total_refund_amount, transaction_sum)

        theoretical_refund_amount = Decimal(order_item_not_refunded.amount_vat_included)
        self.assertEqual(total_refund_amount, theoretical_refund_amount)




