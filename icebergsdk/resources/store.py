# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject

class Store(UpdateableIcebergObject):
    endpoint = 'merchant'
    
    def product_offers(self, params = None, limit = None, offset = 0):
        params = params or {}
        params.update({
            'merchant': self.id,
            'offset': offset
        })
        if limit:
            params['limit'] = limit
        return self.get_list('productoffer', args = params)

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def addresses(self, params = None, limit = None, offset = 0):
        """
        Return merchant addresses/contact info
        """
        params = params or {}
        params.update({
            'merchant': self.id,
            'offset': offset
        })
        if limit:
            params['limit'] = limit
        return self.get_list('merchant_address', args = params)


    def import_products(self, feed_url = None):
        """
        Return product from XML file
        Use for initial import
        """
        feed_url = feed_url or ("%sdownload_export/" % self.resource_uri)

        from icebergsdk.parser import XMLParser

        parser = XMLParser()

        res = []

        for element in parser.parse_feed(feed_url):
            if type(element) != dict:
                raise Exception("element from export feed invalid: %s" % element)
            res.append(UpdateableIcebergObject.findOrCreate(element))

        return res

    def check_activation(self):
        data = self.request("%s%s/" % (self.resource_uri, 'check_activation'), method = "get")
        return data

    def reactivate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'reactivate'), method = "post")
        return self._load_attributes_from_response(**data)

    def pause(self):
        data = self.request("%s%s/" % (self.resource_uri, 'pause'), method = "post")
        return self._load_attributes_from_response(**data)

    def stop(self):
        data = self.request("%s%s/" % (self.resource_uri, 'stop'), method = "post")
        return self._load_attributes_from_response(**data)

    def feeds(self, **filters):
        filters["merchant"] = self.id
        return self.get_list(MerchantFeed.endpoint, args = filters)


class MerchantAddress(UpdateableIcebergObject):
    endpoint = 'merchant_address'

class StoreBankAccount(UpdateableIcebergObject):
    endpoint = 'store_bank_account'

class MerchantImage(IcebergObject):
    endpoint = 'merchant_image'

    def build_resized_image_url(self, width, height, process_mode="crop"):
        from icebergsdk.utils.image_server_utils import build_resized_image_url
        image_server_url = self.__class__._handler.conf.IMAGE_SERVER_URL
        return build_resized_image_url(image_server_url, self.image_path, width, height, process_mode)


class MerchantCommissionSettings(UpdateableIcebergObject):
    endpoint = 'commission_settings'


class MerchantFeed(UpdateableIcebergObject):
    endpoint = 'merchant_catalog_feed'
