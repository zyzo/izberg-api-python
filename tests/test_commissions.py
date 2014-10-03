# -*- coding: utf-8 -*-


from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils

class CommissionsTestCase(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login_user_1(handler = cls.api_handler)
        # Create an application
        application = cls.api_handler.Application()
        application.name = "test-webhook-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)
        cls.my_context_dict['application_token'] = application.auth_me()

        # Create a merchant
        merchant = cls.api_handler.Store()
        merchant.name = "Test Webhook Merchant"
        merchant.application = application
        merchant.save()
        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)
        

        commission_settings = cls.api_handler.MerchantCommissionSettings()
        commission_settings.merchant = merchant
        commission_settings.cpa = 25
        commission_settings.save()
        cls.my_context_dict['commission_settings'] = commission_settings
        cls._objects_to_delete.append(commission_settings)

        cls.api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True) # Connect as staff
        application_settings = cls.api_handler.ApplicationCommissionSettings()
        application_settings.application = application.resource_uri
        application_settings.merchant = merchant.resource_uri
        application_settings.revenue_sharing = 50
        application_settings.save()
        cls.my_context_dict['application_settings'] = application_settings
        cls._objects_to_delete.append(application_settings)





    def test_full_order(self):
        self.login()

        cart = self.api_handler.Cart()
        cart.save()
        
        # offer = cls.my_context_dict['offer']
     
        # cart.addOffer(offer)

        # cart.fetch()

        # addresses = self.api_handler.me().addresses()

        # if len(addresses)==0:
        #     address = self.create_user_address()
        # else:
        #     address = addresses[0]

        # cart.shipping_address = address

        # if cart.has_changed():
        #     cart.save()

        # self.assertEqual(cart.status, "20") # Valide

        # order = cart.createOrder()
        # order.authorizeOrder()



        
