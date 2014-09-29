# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils

class MessagesTest(IcebergUnitTestCase):
    """
    Create an app, a seller and two users
    """
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login_user_1(handler = cls.api_handler)

        # Create an application
        application = cls.api_handler.Application()
        application.name = "test-messages-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)

        # Create a merchant
        merchant = cls.api_handler.Store()
        merchant.name = "Test Message Merchant"
        merchant.application = application
        merchant.save()

        cls.my_context_dict['merchant'] = merchant
        cls._objects_to_delete.append(merchant)

        cls.my_context_dict['application_token'] = application.auth_me()

    def setUp(self):
        pass


    # User - App
    def test_01_user_to_app_messages(self):
        """
        User -> App
        """
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        message = self.api_handler.Message()

        message.sender = self.api_handler.me()
        message.receiver = self.my_context_dict['application']
        
        message.subject = "Test"
        message.body = "Test Body"

        message.save()

        application = self.my_context_dict['application']
        messages = application.inbox()

        found = False

        for applicaton_message in messages:
            if applicaton_message.id == message.id:
                found = True
                self.assertEqual(applicaton_message.subject, message.subject)
                self.assertEqual(applicaton_message.body, message.body)

        self.assertTrue(found)



    def test_02_app_to_user_messages(self):
        """
        App -> User
        """
        pass

    # Seller - App
    def test_03_seller_to_app_messages(self):
        """
        Seller -> App
        """
        pass

    def test_04_app_to_seller_messages(self):
        """
        App -> Seller
        """
        pass

    # Seller - User
    def test_05_seller_to_user_messages(self):
        """
        Seller -> User
        """
        pass

    def test_06_user_to_seller_messages(self):
        """
        User -> Seller 
        """
        pass

