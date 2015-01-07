# -*- coding: utf-8 -*-
from decimal import Decimal
from helper import IcebergUnitTestCase

class ProductChannelTests(IcebergUnitTestCase):

    def test_01_application_user_add_to_cart(self):
        """
        Add to cart as login user
        """
        self.login_user_2()
        