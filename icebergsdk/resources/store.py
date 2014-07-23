# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Store(UpdateableIcebergObject):
    endpoint = 'merchant'
    def product_offers(self):
        return self.get_list('productoffer', args = {'merchant': self.id})
    
