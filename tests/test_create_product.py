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
        application.name = "test-create-product-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)

        # Create a merchant
        merchant = cls.api_handler.Store()
        merchant.name = "Test Create Product Merchant"
        merchant.application = application
        merchant.save()

        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)

    def test_01_create_product(self):
        """
        Create a product
        """
        self.direct_login_user_1()

        product = self.create_product(
                    name = "Test Product",
                    description = "Description of my test product",
                    gender = "W",
                    categories=[50], # chemisier 
                    brand=1
                )
        self.my_context_dict['product'] = product


    def test_02_create_offer(self):
        """
        Create an offer (with no variation)
        """
        self.direct_login_user_1()

        productoffer = self.create_product_offer(
                        product = self.my_context_dict['product'],
                        merchant = self.my_context_dict['merchant'],
                        sku = self.get_random_sku(),
                        image_paths = ["./tests/static/image_test.JPEG"]
                    )

        self.my_context_dict['offer'] = productoffer


    def test_03_create_abstract_offer(self):
        """
        Create an abstract offer (with variation)
        """
        self.direct_login_user_1()

        productoffer = self.api_handler.ProductOffer()

        productoffer = self.create_product_offer(
                        product = self.my_context_dict['product'],
                        merchant = self.my_context_dict['merchant'],
                        is_abstract= True,
                        image_paths = ["./tests/static/image_test.JPEG"]
                    )
        self.my_context_dict['abstract_offer'] = productoffer


        productvariation = self.create_product_variation(
                        product_offer = productoffer,
                        sku = self.get_random_sku(),
                        variation_type = ["color", "size"],
                        name = "Red Small",
                        price = 75.5,
                        stock = 20,
                        size = "Small",
                    )

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
