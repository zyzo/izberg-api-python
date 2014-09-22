# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from icebergsdk.exceptions import IcebergClientError

class ClientCreateProduct(IcebergUnitTestCase):

    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls.objects_to_delete = []
        
        api_handler = get_api_handler()
        api_handler.auth_user(username="jeffstrongman", email="user1@iceberg-marketplace.com")

        # Create an application
        application = cls.class_create_application(api_handler=api_handler)
        cls.objects_to_delete.append(application)
        cls.my_context_dict["application"] = application

        # Create a merchant
        merchant = cls.class_create_merchant(api_handler=api_handler, application=application)
        cls.my_context_dict["merchant"] = merchant
        cls.objects_to_delete.append(merchant)


    def test_01_create_product(self):
        """
        Create a product
        """
        product = self.api_handler.Product()
        product.name = "Test Product"
        product.description = "Description of my product"
        product.gender = "W" # Woman

        product.save() # Need to save before assign categories
        self.objects_to_delete.append(product)

        chemise_chemisier_category = self.api_handler.Category()
        chemise_chemisier_category.id = 50 # Just to be able to 
        product.categories = [chemise_chemisier_category]


        brand = self.api_handler.Brand()
        brand.id = 1
        product.brand = brand
        
        product.save()

        self.my_context_dict['product'] = product

    def setUp(self):
        super(ClientCreateProduct, self).setUp()
        self.direct_login_user_1()

    def test_02_create_offer(self):
        """
        Create an offer (with no variation)
        """
        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.sku = self.get_random_sku()
        productoffer.save()
        self.objects_to_delete.append(productoffer)
        self.my_context_dict['offer'] = productoffer


    def test_03_create_abstract_offer(self):
        """
        Create an abstract offer (with variation)
        """
        productoffer = self.api_handler.ProductOffer()

        productoffer.product = self.my_context_dict['product']
        productoffer.merchant = self.my_context_dict['merchant']
        productoffer.is_abstract = True
        productoffer.save()
        self.objects_to_delete.append(productoffer)
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

        self.objects_to_delete.append(productvariation)
        self.my_context_dict['productvariation'] = productvariation


    def test_04_activate_offer(self):
        """
        Activate the offer
        """
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


    # def test_06_modify_product(self):
    #     """
    #     Remove the category of the product to check if the statuses change to draft
    #     """
    #     product = self.my_context_dict['product']
    #     productoffer = self.my_context_dict['abstract_offer']
    #     productvariation = self.my_context_dict['productvariation']
    #     product.categories = []
    #     product.save()
    #     self.assertEqual(product.status, "draft")
    #     productoffer.fetch()
    #     self.assertEqual(productoffer.status, "draft")
    #     productvariation.fetch()
    #     self.assertEqual(productvariation.status, "draft")


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "objects_to_delete"):
            api_handler = get_api_handler()
            api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True)

            for obj in cls.objects_to_delete:
                try:
                    obj.delete(handler = api_handler)
                    # print "obj %s deleted" % obj
                except:
                    pass
                    # print "couldnt delete obj %s" % obj

