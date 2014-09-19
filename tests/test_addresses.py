# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase

class ClientAddresses(IcebergUnitTestCase):
    def test_create(self):
        """
        Create an address for the user
        """
        self.login()
        self.create_user_address()


    def test_read(self):
        """
        Try to fetch the address created before
        """
        self.login()

        addresses = self.api_handler.me().addresses()

        self.assertNotEqual(len(addresses), 0)




