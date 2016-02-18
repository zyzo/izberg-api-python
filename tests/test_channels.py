# -*- coding: utf-8 -*-
import random
from decimal import Decimal
from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils

class ProductChannelTests(IcebergUnitTestCase):

    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login_user_1(handler = cls.api_handler)
        # Create an application
        application = cls.api_handler.Application()
        application.name = "test-product-channel"
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
        merchant.name = "Test Product Channel Merchant"
        merchant.application = application
        merchant.save()
        merchant.reactivate()
        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)

        merchant_address = cls.api_handler.MerchantAddress()
        merchant_address.merchant = merchant
        merchant_address.contact_email = "contact+api-test-product-channel@izberg-marketplace.com"
        merchant_address.address = "325 random street"
        merchant_address.city = "Paris"
        merchant_address.zipcode = "75012"
        merchant_address.phone = "0123281398"
        merchant_address.country = cls.api_handler.Country.search({'code': 'FR'})[0][0]
        merchant_address.save()
        cls.my_context_dict['merchant_address'] = merchant_address
        cls._objects_to_delete.append(merchant_address)

        merchant_feed = cls.api_handler.MerchantFeed()
        merchant_feed.feed_url = "http://s3-eu-west-1.amazonaws.com/static.iceberg.com/xsd/examples/hightech_example.xml"
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


    def test_01_test_merchant_backoffice_channel_auto_sync(self):
        """ The backoffice channel of the merchant is automatically synced """
        merchant = self.my_context_dict['merchant']
        
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        backoffice_channel = merchant.backoffice_channel
        self.assertTrue(backoffice_channel.wait_for_value('status', 'synced', max_wait=300))


    
    def test_02_test_merchant_active_products_channel_auto_sync(self):
        """ The active products channel of the merchant is automatically synced """
        merchant = self.my_context_dict['merchant']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = merchant.active_products_channel
        self.assertTrue(active_products_channel.wait_for_value('status', 'synced', max_wait=300))


    def test_03_test_application_backoffice_channel_auto_sync(self):
        """ The backoffice channel of the application is automatically synced """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        backoffice_channel = application.backoffice_channel
        self.assertTrue(backoffice_channel.wait_for_value('status', 'synced', max_wait=300))
    

    def test_04_test_application_active_products_channel_auto_sync(self):
        """ The active products channel of the application is automatically synced """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = application.active_products_channel
        self.assertTrue(active_products_channel.wait_for_value('status', 'synced', max_wait=300))


    def test_05_test_merchant_backoffice_channel_contains_products_in_storage(self):
        """ The backoffice channel of the merchant contains products in storage backend """
        merchant = self.my_context_dict['merchant']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        backoffice_channel = merchant.backoffice_channel
        self.assertTrue(len(backoffice_channel.get_products())>0)


    def test_06_test_merchant_active_products_channel_contains_products_in_storage(self):
        """ The active products channel of the application contains products in storage backend """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = application.active_products_channel
        self.assertTrue(len(active_products_channel.get_products())>0)


    def test_07_test_application_backoffice_channel_contains_products_in_storage(self):
        """ The backoffice channel of the application contains products in storage backend """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        backoffice_channel = application.backoffice_channel
        self.assertTrue(len(backoffice_channel.get_products())>0)


    def test_08_test_application_active_products_channel_contains_products_in_storage(self):
        """ The active products channel of the application contains products in storage backend """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = application.active_products_channel
        self.assertTrue(len(active_products_channel.get_products())>0)


    def test_09_test_merchant_backoffice_channel_contains_products_in_algolia(self):
        """ The backoffice channel of the merchant contains products in algolia output """
        merchant = self.my_context_dict['merchant']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        backoffice_channel = merchant.backoffice_channel
        self.assertTrue(len(backoffice_channel.algolia_search(""))>0)


    def test_10_test_merchant_active_products_channel_contains_products_in_algolia(self):
        """ The active products channel of the application contains products in algolia output """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = application.active_products_channel
        self.assertTrue(len(active_products_channel.algolia_search(""))>0)


    def test_11_test_application_backoffice_channel_contains_products_in_algolia(self):
        """ The backoffice channel of the application contains products in algolia output """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        backoffice_channel = application.backoffice_channel
        self.assertTrue(len(backoffice_channel.algolia_search(""))>0)


    def test_12_test_application_active_products_channel_contains_products_in_algolia(self):
        """ The active products channel of the application contains products in algolia output """
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        active_products_channel = application.active_products_channel
        self.assertTrue(len(active_products_channel.algolia_search(""))>0)



    def test_13_test_name_description_price_stock_are_coherent_on_storage(self):
        """ The attributes name/description/price/stock are the same for the offer resource and in the channel storage  """
        application = self.my_context_dict['application']
        offer = self.my_context_dict['offer']
        product = offer.product
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        backoffice_channel = application.backoffice_channel
        raw_product_from_storage = backoffice_channel.get_product(offer.product.id, raw_result=True)
        raw_best_offer = raw_product_from_storage.get("best_offer", {})
        self.assertFalse(raw_best_offer is None)
        self.assertEqual(product.name, raw_product_from_storage.get("name"))
        self.assertEqual(product.description, raw_product_from_storage.get("description"))
        self.assertEqual(Decimal(offer.price_with_vat), Decimal(raw_best_offer.get("price_with_vat")))
        self.assertEqual(offer.stock, raw_best_offer.get("stock"))


    def test_14_test_name_description_price_stock_are_coherent_on_algolia(self):
        """ The attributes name/description/price/stock are the same for the offer resource and in the channel algolia output  """
        offer = self.my_context_dict['offer']
        product = offer.product
        application = self.my_context_dict['application']
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        backoffice_channel = application.backoffice_channel
        raw_product_from_algolia = backoffice_channel.algolia_find(offer.product.id, raw_result=True)
        raw_best_offer = raw_product_from_algolia.get("best_offer", {})
        self.assertFalse(raw_best_offer is None)
        self.assertEqual(product.name, raw_product_from_algolia.get("name"))
        self.assertEqual(product.description, raw_product_from_algolia.get("description"))
        self.assertEqual(Decimal(offer.price_with_vat), Decimal(raw_best_offer.get("price_with_vat")))
        self.assertEqual(offer.stock, raw_best_offer.get("stock"))


    def test_15_test_changing_the_name_of_the_product_changes_it_on_storage(self):
        """ Changing the name of product changes on storage """
        application = self.my_context_dict['application']
        offer = self.my_context_dict['offer']
        product = offer.product
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        backoffice_channel = application.backoffice_channel

        backoffice_channel._handler.lang = backoffice_channel.language
        new_name = u"Nëw Randôm Nàme %s" % random.randint(1,1000)
        product.name = new_name
        product.save()
        product.fetch()
        self.assertEqual(product.name, new_name)
        self.assertTrue(backoffice_channel.storage_wait_for_value(product.id, "name", new_name))


    def test_16_test_changing_the_name_of_the_product_changes_it_on_algolia(self):
        """ Changing the name of offer changes on algolia  """
        application = self.my_context_dict['application']
        offer = self.my_context_dict['offer']
        product = offer.product
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        backoffice_channel = application.backoffice_channel

        backoffice_channel._handler.lang = backoffice_channel.language
        new_name = u"Nëw Randôm Nàme %s" % random.randint(1,1000)
        offer.name = new_name
        offer.save()
        offer.fetch()
        self.assertEqual(offer.name, new_name)
        self.assertTrue(backoffice_channel.algolia_wait_for_value(product.id, "best_offer.name", new_name))


    def test_16_test_changing_the_price_of_the_product_changes_it_on_algolia(self):
        """ Changing the price of offer (with no variation) changes the price on algolia """
        application = self.my_context_dict['application']
        merchant = self.my_context_dict['merchant']
        offers_with_no_variations = merchant.product_offers(params={"is_abstract":False})
        self.assertTrue(len(offers_with_no_variations)>0)
        offer = offers_with_no_variations[0]
        product = offer.product
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        backoffice_channel = application.backoffice_channel

        backoffice_channel._handler.lang = backoffice_channel.language
        new_price = Decimal(str(random.randint(500000,100000000)/1000000.))
        # if offer.variations:
        #     variation = offer.variation[0]
        #     variation.price = new_price
        #     variation.save()
        #     variation.fetch()
        #     self.assertEqual(variation.price, new_price)
        # else:
        offer.price = new_price
        offer.save()
        offer.fetch()
        self.assertEqual(offer.price, new_price)

        self.assertTrue(
            backoffice_channel.algolia_wait_for_value(
                product.id, "best_offer.price_with_vat", offer.price_with_vat, process_functions=[str, Decimal]
            )
        )
        self.assertTrue(
            backoffice_channel.algolia_wait_for_value(
                product.id, "best_offer.price", offer.price, process_functions=[str, Decimal]
            )
        )
        self.assertTrue(
            backoffice_channel.algolia_wait_for_value(
                product.id, "best_offer.price_without_vat", offer.price_without_vat, process_functions=[str, Decimal]
            )
        )



