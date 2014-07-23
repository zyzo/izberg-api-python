# -*- coding: utf-8 -*-


from icebergsdk.resources.base import UpdateableIcebergObject

class Product(UpdateableIcebergObject):
    endpoint = 'product'

class ProductOffer(UpdateableIcebergObject):
    endpoint = 'productoffer'

class ProductVariation(UpdateableIcebergObject):
    endpoint = 'product_variation'


