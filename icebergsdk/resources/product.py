# -*- coding: utf-8 -*-


from icebergsdk.resources.base import UpdateableIcebergObject, IcebergObject

"""
Todo: Add addToCart method to ProductOffer and ProductVariation

"""

class Product(UpdateableIcebergObject):
    endpoint = 'product'

    def reviews(self):
        return self.get_list('review', args = {'product': self.id})


class ProductOffer(UpdateableIcebergObject):
    endpoint = 'productoffer'

    def activate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'activate'), method = "post")
        return self._load_attributes_from_response(**data)

    def deactivate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'deactivate'), method = "post")
        return self._load_attributes_from_response(**data)


class ProductVariation(UpdateableIcebergObject):
    endpoint = 'product_variation'

class ProductOfferImage(UpdateableIcebergObject):
    endpoint = 'offer_image'

class Category(IcebergObject):
    endpoint = 'category'

class Brand(UpdateableIcebergObject):
    endpoint = 'brand'