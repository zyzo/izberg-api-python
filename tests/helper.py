# -*- coding: utf-8 -*-

import os
import unittest

from datetime import datetime

from icebergsdk.conf import ConfigurationDebug, ConfigurationSandbox #, ConfigurationStage
from icebergsdk.api import IcebergAPI

from helpers.objects_shortcuts_mixin import IcebergObjectCreateMixin
from icebergsdk.exceptions import IcebergClientError

def get_api_handler():
    if os.getenv('ICEBERG_DEBUG', False):
        api_handler = IcebergAPI(conf = ConfigurationDebug)
    else:
        api_handler = IcebergAPI(conf = ConfigurationSandbox)

    return api_handler


class IcebergUnitTestCase(unittest.TestCase, IcebergObjectCreateMixin):
    @classmethod
    def setUpClass(cls):
        """
        my_context_dict: Create a context dictionary to share some results between tests
        _objects_to_delete: We will delete the created objects after all tests have been done
        """
        cls.my_context_dict = {}
        cls._objects_to_delete = []


    @classmethod
    def tearDownClass(cls):
        """
        Delete objects created during tests
        """
        if hasattr(cls, "_objects_to_delete"):
            api_handler = get_api_handler()
            api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True) # Connect as staff
            fail_silently = True
            for obj in cls._objects_to_delete:
                try:
                    obj.delete(handler = api_handler)
                    # print "obj %s deleted" % obj
                except:
                    if not fail_silently:
                        raise
                    # print "couldnt delete obj %s" % obj


    def setUp(self):
        self.setup_api_handler()

    def setup_api_handler(self):
        self.api_handler = get_api_handler()
        self.api_handler._objects_to_delete = []



    ###
    #   Temp, will be moved out
    ###
    def login(self):
        self.api_handler.sso_user(email = "lol@lol.fr", first_name = "Yves", last_name = "Durand")

    def login_anonymous(self):
        self.api_handler.sso_user()

    def login_user_1(self):
        self.api_handler.sso_user(email = "user1@iceberg-marketplace.com", first_name = "Jeff", last_name = "Strongman")

    def login_user_2(self):
        self.api_handler.sso_user(email = "user2@iceberg-marketplace.com", first_name = "Sara", last_name = "Crôche")

    def direct_login(self):
        self.api_handler.auth_user(username="yvesdurand5269004", email="lol@lol.fr")

    def direct_login_user_1(self):
        self.api_handler.auth_user(username="jeffstrongman", email="user1@iceberg-marketplace.com")

    def direct_login_user_2(self):
        self.api_handler.auth_user(username="saracroche", email="user2@iceberg-marketplace.com")

    def direct_login_iceberg_staff(self):
        self.api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True)



    def full_order(self, offer_ids=None, number_of_offers=1):
        """
        Full order
        """
        self.login()

        cart = self.api_handler.Cart()
        cart.save()
        
        offers = []
        
        if offer_ids:
            for offer_id in offer_ids:
                offers.append(self.api_handler.ProductOffer.find(offer_id))
        else:

            for i in xrange(number_of_offers):
                offers.append(self.get_random_offer())
            

        for offer in offers:
            if hasattr(offer, 'variations') and len(offer.variations) > 0:
                for variation in offer.variations:
                    print variation
                    print variation.to_JSON()
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

        api_user = self.api_handler.User.me()

        try:
            form_data = cart.form_data()
        except IcebergClientError, e:
            if 90001 in e.error_codes and api_user.is_staff: # User Birthday
                profile = api_user.profile()
                profile.birth_date = datetime.strptime('Jun 3 1980', '%b %d %Y')
                profile.save()

                form_data = cart.form_data()
            else:
                raise e

        order = cart.createOrder({
            'pre_auth_id': form_data['id']
        })

        # Create Card Alias
        import urllib, urllib2

        url = form_data['CardRegistrationURL']

        params = {
            "data": form_data['PreregistrationData'],
            "accessKeyRef": form_data['AccessKey'],
            "cardNumber": "4970101122334471",
            "cardExpirationDate": "1015", # Should be in the future
            "cardCvx": "123"
        }
        params_enc = urllib.urlencode(params)
        request = urllib2.Request(url, params_enc)
        page = urllib2.urlopen(request)
        content = page.read()
        card_registration_data = content.replace('data=', '')

        print card_registration_data

        order.authorizeOrder({
            "data": card_registration_data
        })

        if hasattr(order.payment, 'redirect_url'): # 3D Secure
            print "Need 3D Secure"
            self.pass_3d_secure_page(order.payment.redirect_url)
            order.updateOrderPayment()

        self.my_context_dict['order'] = order
        self.my_context_dict['merchant_order'] = order.merchant_orders[0]

    def pass_3d_secure_page(self, url):
        import time
        from selenium import webdriver
        driver = webdriver.Chrome()
        try:
            driver.get(url)
            time.sleep(3) # Wait 5 secs to be sure browser will go to step2

            driver.find_element_by_name("password").send_keys('secret3')
            driver.find_element_by_name("submit").click()

            # Waiting (max : 10s) for mangopay redirection to return_url (that test sent - see few lines above )
            # for i in range(10):
            #     if check_string in driver.current_url:
            #         break
            #     else:
            #         time.sleep(1)
            time.sleep(3)
        finally:
            driver.quit()

        return True