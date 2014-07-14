# -*- coding: utf-8 -*-


from icebergsdk.resources.base import IcebergObject

class Product(IcebergObject):
    endpoint = 'product'

class ProductOffer(IcebergObject):
    endpoint = 'productoffer'

class ProductVariation(IcebergObject):
    endpoint = 'product_variation'


