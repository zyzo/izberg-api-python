# -*- coding: utf-8 -*-

import os
import unittest

from icebergsdk.conf import ConfigurationDebug, ConfigurationSandbox #, ConfigurationStage
from icebergsdk.api import IcebergAPI

from helpers.objects_shortcuts_mixin import IcebergObjectCreateMixin


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

