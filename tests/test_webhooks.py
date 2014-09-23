# -*- coding: utf-8 -*-
import time
import json
from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils
import os

class WebhookTestCase(IcebergUnitTestCase):
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
        cls.my_context_dict['application_token'] = application.auth_me()

    def test_01_create_update_webhook(self):
        """
        Create and update a webhook
        """
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        application = self.my_context_dict['application']
        
        webhook = self.create_webhook(application=application, event="new_merchant_available", url="http://api.iceberg.technology")
        webhook.url = webhook.get_test_endpoint_url()
        webhook.save() ## update
        self.my_context_dict['webhook'] = webhook
        self._objects_to_delete.append(webhook)


    def test_02_trigger_test_webhook(self):
        """
        Trigger the test option on the webhook
        """
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']

        webhook = self.my_context_dict['webhook']
        webhook.test_trigger()

        number_of_checks = 10
        webhook_triggers = []
        ## looping to wait for the webhook to be triggered
        while number_of_checks>0 and len(webhook_triggers)==0:
            webhook_triggers = webhook.triggers()
            number_of_checks -= 1
            if not os.getenv('ICEBERG_DEBUG', False): ## in debug, sync >> no need to wait
                time.sleep(5) ## check each 5 seconds
        print "number_of_checks left = %s, webhook_triggers=%s" % (number_of_checks, webhook_triggers)
        self.assertEquals(len(webhook_triggers), 1)
        webhook_trigger = webhook_triggers[0]
        self.assertTrue(webhook_trigger.is_test)
        self.assertEquals(webhook_trigger.status, "succeeded")
        

    def test_03_trigger_new_merchant_available(self):
        """
        Test new_merchant_available triggering when creating a new merchant
        """
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        
        webhook = self.my_context_dict['webhook']
        new_merchant = self.create_merchant(application=self.my_context_dict['application'])
        
        number_of_checks = 10
        webhook_triggers = []
        ## looping to wait for the webhook to be triggered
        while number_of_checks>0 and len(webhook_triggers)<=1:
            webhook_triggers = webhook.triggers()
            number_of_checks -= 1
            if not os.getenv('ICEBERG_DEBUG', False): ## in debug, sync >> no need to wait
                time.sleep(5) ## check each 5 seconds
        print "number_of_checks left = %s, webhook_triggers=%s" % (number_of_checks, webhook_triggers)
        self.assertEquals(len(webhook_triggers), 2)
        webhook_trigger = webhook_triggers[0]
        self.assertFalse(webhook_trigger.is_test)
        self.assertEquals(webhook_trigger.status, "succeeded")
        self.assertEqual(new_merchant.resource_uri, webhook_trigger.payload.resource_uri)


    def test_04_delete_webhook(self):
        """
        Delete the webhook
        """
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        webhook = self.my_context_dict['webhook']
        webhook.delete()
        if webhook in self._objects_to_delete:
            ## no need to delete it in tearDownClass if delete succeeded
            self._objects_to_delete.remove(webhook)

    def test_05_create_product_and_webhook(self):
        self.login_user_1()
        self.api_handler.access_token = self.my_context_dict['application_token']
        application = self.my_context_dict['application']
        
        webhook = self.create_webhook(application=application, event="new_merchant_available", url="http://api.iceberg.technology")
        webhook.url = webhook.get_test_endpoint_url()
        webhook.save() ## update

        self.my_context_dict['webhook_2'] = webhook
        
    def test_05_trigger_product_offer_updated(self):
        """
        Test product_offer_updated triggering when updating a product_offer
        """

        
