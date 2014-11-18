# -*- coding: utf-8 -*-

from decimal import Decimal
from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils

MERCHANT_COMMISSION = Decimal("0.40")
REVENUE_SHARING = Decimal("0.05")
APPLICABLE_TAX_RATE = Decimal("0.20")


class CommissionsTestCase(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login_user_1(handler = cls.api_handler)
        # Create an application
        application = cls.api_handler.Application()
        application.name = "test-commission-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)
        cls.my_context_dict['application_token'] = application.auth_me()

        app_merchant_policies = cls.api_handler.ApplicationMerchantPolicies()
        app_merchant_policies.application = application
        app_merchant_policies.set_mandatory_fields(payment_card=False, products=True, 
                                                   return_info=False, shipping_info=False, 
                                                   store_contact=False, store_information=False,
                                                   store_legal=False)


        # Create a merchant
        merchant = cls.api_handler.Store()
        merchant.name = "Test Commission Merchant"
        merchant.application = application
        merchant.save()
        merchant.reactivate()
        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)


        shipping_policy = cls.api_handler.MerchantShippingPolicy()
        shipping_policy.merchant = merchant
        shipping_policy.shipping_policy = 3
        shipping_policy.code = 1
        shipping_policy.parameters = {"infinite":6}
        shipping_policy.save()
        cls.my_context_dict['shipping_policy'] = shipping_policy
        cls._objects_to_delete.append(shipping_policy)
        

        commission_settings = cls.api_handler.MerchantCommissionSettings()
        commission_settings.merchant = merchant
        commission_settings.cpa = MERCHANT_COMMISSION*100
        commission_settings.save()

        cls.my_context_dict['commission_settings'] = commission_settings
        cls._objects_to_delete.append(commission_settings)

        cls.api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True) # Connect as staff
        application_settings = cls.api_handler.ApplicationCommissionSettings()
        application_settings.application = application
        application_settings.merchant = merchant
        application_settings.revenue_sharing = REVENUE_SHARING*100
        application_settings.applicable_tax_rate = APPLICABLE_TAX_RATE*100
        application_settings.save()
        cls.my_context_dict['application_settings'] = application_settings
        cls._objects_to_delete.append(application_settings)


        merchant_feed = cls.api_handler.MerchantFeed()
        merchant_feed.feed_url = "http://s3-eu-west-1.amazonaws.com/static.iceberg.com/xsd/examples/perfume_example.xml"
        merchant_feed.merchant = merchant
        merchant_feed.source_type = "iceberg"
        merchant_feed.save()
        cls.my_context_dict['merchant_feed'] = merchant_feed
        cls._objects_to_delete.append(merchant_feed)


        merchant_feed.parse()

        offers = merchant.wait_for_active_offers()
        offer = offers[0]
        cls.my_context_dict['offer'] = offer

        merchant.check_activation()




    def test_01_full_order(self):
        offer = self.my_context_dict['offer']
        
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']


        cart = self.api_handler.Cart()
        cart.save()

        
     
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
            address = self.create_user_address()
        else:
            address = addresses[0]

        cart.shipping_address = address

        if cart.has_changed():
            cart.save()

        self.assertEqual(cart.status, "20") # Valide

        order = cart.createOrder()
        order.authorizeOrder()

        merchant_order = order.merchant_orders[0]
        merchant_order.confirm()

        self.my_context_dict['order'] = order
        self.my_context_dict['merchant_order'] = merchant_order

    def test_02_check_store_commission(self):
        """
        Check store commission amount
        ## NB: ASSUMES a 20%% vat rate
        """
        self.direct_login_iceberg_staff()
        merchant_order = self.my_context_dict['merchant_order']
        order = self.my_context_dict['order']
        transaction = self.api_handler.Transaction.findWhere({"order":order.id})
        self.my_context_dict['transaction'] = transaction
        merchant_transactions = self.api_handler.MerchantTransaction.search(args={"transaction":transaction.id})[0]
        self.assertEqual(len(merchant_transactions), 1)
        merchant_transaction = merchant_transactions[0]
        expected_merchant_commission = ( Decimal(merchant_order.price) + Decimal(merchant_order.vat_on_products) )*(1-MERCHANT_COMMISSION)
        expected_merchant_commission = expected_merchant_commission.quantize(Decimal("0.01"))
        expected_merchant_commission += Decimal(merchant_order.shipping_vat_included) ## adding shipping
        # self.assertEqual(Decimal(merchant_transaction.amount),  expected_merchant_commission)
        difference = abs(expected_merchant_commission-Decimal(merchant_transaction.amount))
        self.assertTrue(difference <= Decimal("0.01"))


    def test_03_check_app_commission(self):
        """
        Check app commission amount
        ## NB: ASSUMES a 20%% vat rate
        """
        self.direct_login_iceberg_staff()
        merchant_order = self.my_context_dict['merchant_order']
        transaction = self.my_context_dict['transaction']
        app_transactions = self.api_handler.ApplicationTransaction.search(args={"transaction":transaction.id})[0]
        self.assertEqual(len(app_transactions), 1)
        app_transaction = app_transactions[0]
        expected_app_commission = (Decimal(merchant_order.price)+Decimal(merchant_order.vat_on_products))*MERCHANT_COMMISSION*(1-REVENUE_SHARING)
        expected_app_commission = expected_app_commission.quantize(Decimal("0.01"))

        # self.assertEqual(Decimal(app_transaction.amount),  expected_app_commission)
        difference = abs(expected_app_commission-Decimal(app_transaction.amount))
        self.assertTrue(difference <= Decimal("0.01"))



    def test_04_check_mp_commission(self):
        """
        Check MP commission amount
        ## NB: ASSUMES a 20%% vat rate
        """
        self.direct_login_iceberg_staff()
        merchant_order = self.my_context_dict['merchant_order']
        transaction = self.my_context_dict['transaction']
        mp_transactions = self.api_handler.MarketPlaceTransaction.search(args={"transaction":transaction.id})[0]
        if REVENUE_SHARING:
            self.assertEqual(len(mp_transactions), 1)
            mp_transaction = mp_transactions[0]
            expected_mp_commission = (Decimal(merchant_order.price)+Decimal(merchant_order.vat_on_products))*MERCHANT_COMMISSION*REVENUE_SHARING
            expected_mp_commission = expected_mp_commission.quantize(Decimal("0.01"))
            # self.assertEqual(Decimal(mp_transaction.amount),  expected_mp_commission)
            difference = abs(expected_mp_commission-Decimal(mp_transaction.amount))
            self.assertTrue(difference <= Decimal("0.01"))
        else:
            self.assertEqual(len(mp_transactions), 0)






        
