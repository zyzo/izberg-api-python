# -*- coding: utf-8 -*-

import unittest
from icebergsdk.api import IcebergAPI

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.api_handler = IcebergAPI()
        
    def test_sso(self):
        user = self.api_handler.sso("lol@lol.fr", "Yves", "Durand")
        self.assertEquals(user.first_name, "Yves")

    def test_Coucou(self):
        self.assertEquals(2, 2)

    def test_cartInfos(self):
        user_cart = self.api_handler.Cart.mine()
        # self.assertEquals(user_cart, "Yves")
        # print user_cart.shipping_address
        # print user_cart.total_amount
        # print user_cart.estimated_shipping_country





