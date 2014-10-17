# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase

class ClientProductImport(IcebergUnitTestCase):    
    """
    Test the XML product import for a store
    """
    def test_import(self):
    	"""
        Product import from a random catalog
        """
        self.login()

        store = self.get_random_active_store()

        products = store.import_products()

        self.assertNotEqual(len(products), 0)




