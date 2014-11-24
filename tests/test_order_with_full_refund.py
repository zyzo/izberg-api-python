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

    def test_02_full_order(self):
        """
        Full order
        """
        self.full_order(number_of_offers=3)

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
        for order_item in merchant_order.items:
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
        
    def test_05_accept_return(self):
        """
        Accept Return Requests
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        for return_request in return_requests:
            return_request.accept()
        
        
    def test_06_create_full_refund(self):
        """
        Create Full Refund
        """
        self.login()
        return_requests = self.my_context_dict['return_requests']
        merchant_order = self.my_context_dict['merchant_order']
        refund = self.api_handler.Refund()
        refund.return_requests = return_requests
        refund.merchant_order = merchant_order
        refund.merchant = merchant_order.merchant
        refund.user = self.api_handler.User.me()
        refund.partial_refund = False
        refund.shipping = merchant_order.shipping_vat_included
        refund.adjustment = 0
        refund.memo = u"Mémô"
        refund.seller_note = u"Séllèr Nötè" 
        refund.sync = True
        refund.save()
        self.my_context_dict['refund'] = refund

        # theoretical_amount = sum([Decimal(return_request.order_item.amount_vat_included) for return_request in return_requests])
        self.assertEqual(Decimal(refund.amount), Decimal(merchant_order.price_vat_included)) ## product price vat included
        self.assertEqual(Decimal(refund.total_refund_amount), Decimal(merchant_order.amount_vat_included)) ## total amounts

        self.assertEqual(refund.status, "complete")
        

    def test_07_check_transactions(self):
        """
        Check Refund Transactions
        """
        self.direct_login_iceberg_staff()

        order = self.my_context_dict['order']
        refund = self.my_context_dict['refund']

        sell_transaction = self.api_handler.Transaction.findWhere({"order":order.id, "transaction_type":1})

        app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":sell_transaction.id})[0]
        self.assertEqual(len(app_transactions), 1)
        app_sell_transaction = app_transactions[0]

        merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":sell_transaction.id})[0]
        self.assertEqual(len(merchant_transactions), 1)
        merchant_sell_transaction = merchant_transactions[0]

        mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":sell_transaction.id})[0]
        has_revenue_sharing = len(mp_transactions) > 0 ## if we find some mp_transactions, there should be revenue sharing
        if has_revenue_sharing:
            self.assertEqual(len(mp_transactions), 1)
            mp_sell_transaction = mp_transactions[0]



        refund_transaction = self.api_handler.Transaction.findWhere({"order":order.id, "transaction_type":2})

        app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(app_transactions), 1)
        app_refund_transaction = app_transactions[0]

        merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":refund_transaction.id})[0]
        self.assertEqual(len(merchant_transactions), 1)
        merchant_refund_transaction = merchant_transactions[0]

        mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":refund_transaction.id})[0]
        if has_revenue_sharing:
            self.assertEqual(len(mp_transactions), 1)
            mp_refund_transaction = mp_transactions[0]
        else:
            self.assertEqual(len(mp_transactions), 0)


        transaction_sum = Decimal(app_refund_transaction.amount) + Decimal(merchant_refund_transaction.amount)
        if has_revenue_sharing:
            transaction_sum += Decimal(mp_refund_transaction.amount)
        transaction_sum = - transaction_sum

        total_refund_amount = Decimal(refund.total_refund_amount)
        self.assertEqual(total_refund_amount, transaction_sum)

        self.assertEqual(total_refund_amount, Decimal(order.amount_vat_included))
    
        self.assertEqual(Decimal(app_sell_transaction.amount), -Decimal(app_refund_transaction.amount))
        self.assertEqual(Decimal(merchant_sell_transaction.amount), -Decimal(merchant_refund_transaction.amount))
        if has_revenue_sharing:
            self.assertEqual(Decimal(mp_sell_transaction.amount), -Decimal(mp_refund_transaction.amount))











