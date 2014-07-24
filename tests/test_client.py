# -*- coding: utf-8 -*-

import unittest
from icebergsdk.api import IcebergAPI

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.api_handler = IcebergAPI()
        
    def test_sso(self):
        user = self.api_handler.sso("lol@lol.fr", "Yves", "Durand")
        print user.__dir__



