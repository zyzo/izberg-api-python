# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils

class ClientCreateProduct(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login(handler = cls.api_handler)

        application = cls.api_handler.Application()
        application.name = "test-merchant-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)

        merchant = cls.api_handler.Store()
        merchant.name = "Test Merchant Create Product"
        merchant.application = application
        merchant.save()

        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)


    def setUp(self):
        pass

    def test_01_create_product(self):
        product = self.api_handler.Product()
        product.name = "Test Product"
        product.description = "Description of my product"
        product.gender = "W" # Woman

        product.save() # Need to save before assign categories
        self._objects_to_delete.append(product)

        chemise_chemisier_category = self.api_handler.Category()
        chemise_chemisier_category.id = 50 # Just to be able to 
        
        product.categories = [chemise_chemisier_category]
        product.save()

        self.my_context_dict['product'] = product


    def test_02_create_offer(self):
        """
        Once we have a Product, create an offer
        """
        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.sku = self.get_random_sku()

        productoffer.save()
        self._objects_to_delete.append(productoffer)


    def test_03_create_variations(self):
        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.is_abstract = True
        productoffer.save()

        productvariation = self.api_handler.ProductVariation()
        productvariation.name = "Small"
        productvariation.sku = self.get_random_sku()
        productvariation.product_offer = productoffer
        productvariation.stock = 20
        productvariation.save()

        self._objects_to_delete.append(productvariation)




