# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from icebergsdk.exceptions import IcebergClientError
from helpers.login_utils import IcebergLoginUtils

class ClientCreateProduct(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login_user_1(handler = cls.api_handler)
        # Create an application
        application = cls.api_handler.Application()
        application.name = "test-merchant-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)

        # Create a merchant
        merchant = cls.api_handler.Store()
        merchant.name = "Test Merchant Create Product"
        merchant.application = application
        merchant.save()

        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)

    def test_01_create_product(self):
        """
        Create a product
        """
        self.direct_login_user_1()

        product = self.api_handler.Product()
        product.name = "Test Product"
        product.description = "Description of my product"
        product.gender = "W" # Woman

        product.save() # Need to save before assign categories
        self._objects_to_delete.append(product)

        chemise_chemisier_category = self.api_handler.Category()
        chemise_chemisier_category.id = 50 # Just to be able to 
        product.categories = [chemise_chemisier_category]


        brand = self.api_handler.Brand()
        brand.id = 1
        product.brand = brand
        
        product.save()

        self.my_context_dict['product'] = product


    def test_02_create_offer(self):
        """
        Create an offer (with no variation)
        """
        self.direct_login_user_1()

        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.sku = self.get_random_sku()
        productoffer.save()
        self._objects_to_delete.append(productoffer)
        self.my_context_dict['offer'] = productoffer


    def test_03_create_abstract_offer(self):
        """
        Create an abstract offer (with variation)
        """
        self.direct_login_user_1()

        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.is_abstract = True
        productoffer.save()
        self._objects_to_delete.append(productoffer)
        self.my_context_dict['abstract_offer'] = productoffer

        productvariation = self.api_handler.ProductVariation()
        productvariation.name = "Red Small"
        productvariation.variation_type = ["color", "size"]
        productvariation.size = "Small"
        productvariation.sku = self.get_random_sku()
        productvariation.product_offer = productoffer
        productvariation.stock = 20
        productvariation.price = 75.5
        productvariation.save()

        self._objects_to_delete.append(productvariation)
        self.my_context_dict['productvariation'] = productvariation


    def test_04_activate_offer(self):
        """
        Activate the offer
        """
        self.direct_login_user_1()

        productoffer = self.my_context_dict['offer']
        try:
            productoffer.activate()
        except IcebergClientError:
            pass
            # it was expected, price is missing
        else:
            raise Exception("productoffer activation should have failed because price is missing")
        
        productoffer.price = 75.5
        productoffer.save() 
        productoffer.activate() ## now should work


    def test_05_activate_abstract_offer(self):
        """
        Activate the abstract offer
        """
        self.direct_login_user_1()

        productoffer = self.my_context_dict['abstract_offer']
        productvariation = self.my_context_dict['productvariation']
        try:
            productoffer.activate()
        except IcebergClientError:
            ## it was expected, color is missing
            pass
        else:
            raise Exception("productoffer activation should have failed because color is missing")

        productvariation.color = "Red"
        productvariation.save() 
        productoffer.activate() ## now should work

        self.assertEqual(productoffer.status, "active")
        productvariation.fetch()
        self.assertEqual(productvariation.status, "active")


    def test_06_modify_product(self):
        """
        Remove the category of the product to check if the statuses change to draft
        """
        self.direct_login_user_1()
        
        product = self.my_context_dict['product']
        productoffer = self.my_context_dict['abstract_offer']
        productvariation = self.my_context_dict['productvariation']
        product.categories = []
        product.save()
        self.assertEqual(product.status, "draft")
        productoffer.fetch()
        self.assertEqual(productoffer.status, "draft")
        productvariation.fetch()
        self.assertEqual(productvariation.status, "draft")
