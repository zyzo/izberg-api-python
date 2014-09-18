# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler


class ClientCreateProduct(IcebergUnitTestCase):

    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

    def setUp(self):
        super(ClientCreateProduct, self).setUp()

        # Log Direct User
        self.direct_login_user_1()
        # Create an application
        self.application = self.create_application()
        self._objects_to_delete.append(self.application)

        # Create a merchant
        self.merchant = self.create_merchant(application = self.application)
        self._objects_to_delete.append(self.merchant)


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
        productoffer.merchant = self.merchant
        productoffer.sku = self.get_random_sku()

        productoffer.save()
        self._objects_to_delete.append(productoffer)


    def test_03_create_variations(self):
        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.merchant
        productoffer.is_abstract = True
        productoffer.save()

        productvariation = self.api_handler.ProductVariation()
        productvariation.name = "Small"
        productvariation.sku = self.get_random_sku()
        productvariation.product_offer = productoffer
        productvariation.stock = 20
        productvariation.save()

        self._objects_to_delete.append(productvariation)


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "_objects_to_delete"):
            api_handler = get_api_handler()
            api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True)

            for obj in cls._objects_to_delete:
                try:
                    obj.delete(handler = api_handler)
                    # print "obj %s deleted" % obj
                except:
                    pass
                    # print "couldnt delete obj %s" % obj

