# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase

class ClientAddresses(IcebergUnitTestCase):
    def test_create(self):
        self.login()
        self.create_user_address()


    def test_read(self):
        self.login()

        addresses = self.api_handler.me().addresses()

        self.assertNotEqual(len(addresses), 0)




