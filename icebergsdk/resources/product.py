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

    def add_image(self, image_path):
        data = self.send_image(
            path="%s%s/" % (self.resource_uri, 'add_image'),
            image_path=image_path
            )
        return ProductOfferImage()._load_attributes_from_response(**data)

class ProductVariation(UpdateableIcebergObject):
    endpoint = 'product_variation'

class ProductOfferImage(UpdateableIcebergObject):
    endpoint = 'offer_image'

    def build_resized_image_url(self, width, height, process_mode="crop"):
        from icebergsdk.utils.image_server_utils import build_resized_image_url
        image_server_url = self._handler.conf.IMAGE_SERVER_URL
        return build_resized_image_url(image_server_url, self.image_path, width, height, process_mode)

class Brand(UpdateableIcebergObject):
    endpoint = 'brand'


class Category(IcebergObject):
    endpoint = 'category'

    def children(self, params = None, limit = None, offset = 0):
        params = params or {}
        params.update({
            'parents': self.id,
            'offset': offset
        })
        if limit:
            params['limit'] = limit
        return self.get_list('category', args = params)



class ProductFamily(UpdateableIcebergObject):
    endpoint = 'product_family'

    def add_selector(self, family_selector):
        post_args = {
            "selector_id":family_selector.id
        }
        data = self.request("%s%s/" % (self.resource_uri, 'selectors'), method = "post", post_args=post_args)

        self.selectors = []
        for selector in data["objects"]:
            self.selectors.append(ProductFamilySelector.findOrCreate(self._handler,selector))

        return self

    def remove_selector(self, family_selector):
        post_args = {
            "selector_id":family_selector.id
        }
        data = self.request("%s%s/" % (self.resource_uri, 'selectors'), method = "delete", post_args=post_args)

        self.selectors = []
        for selector in data["objects"]:
            self.selectors.append(ProductFamilySelector.findOrCreate(self._handler,selector))

        return self


    def get_products(self, limit=20, offset=0):
        params = {
            "offset":offset,
            "limit":limit
        }
        return self.get_list("%s%s/" % (self.resource_uri, 'products'), args = params)


    def get_stats(self, limit=20, offset=0):
        return self.request("%s%s/" % (self.resource_uri, 'stats'))



class ProductFamilySelector(UpdateableIcebergObject):
    endpoint = 'product_family_selector'
