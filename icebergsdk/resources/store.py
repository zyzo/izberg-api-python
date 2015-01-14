# -*- coding: utf-8 -*-
import time
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

    # Messages
    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def outbox(self):
        return self.get_list("%soutbox/" % self.resource_uri)

    # Addresses
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
            res.append(UpdateableIcebergObject.findOrCreate(self._handler, element))

        return res

    def check_activation(self):
        data = self.request("%s%s/" % (self.resource_uri, 'check_activation'), method = "get")
        return data


    # Transactions
    def reactivate(self, **kwargs):
        data = self.request("%s%s/" % (self.resource_uri, 'reactivate'), method = "post", args=kwargs)
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


    def wait_for_active_offers(self, number_of_active_offers_expected=1, max_number_of_checks=10, check_every_seconds=5):
        active_offers = []
        ## looping to wait for the webhook to be active_offered
        number_of_attempts = 0
        while number_of_attempts<max_number_of_checks and len(active_offers)<number_of_active_offers_expected:
            if number_of_attempts > 0:
                time.sleep(check_every_seconds) ## check every X seconds except the 1st time
            active_offers = self.product_offers(params={"status":"active"})
            number_of_attempts += 1
        print "number_of_attempts = %s, active_offers=%s" % (number_of_attempts, active_offers)
        return active_offers


    @property
    def backoffice_channel(self):
        if not hasattr(self, "_backoffice_channel"):
            data = self.request("%s%s/" % (self.resource_uri, 'backoffice_channel'), method = "get")
            self._backoffice_channel = UpdateableIcebergObject.findOrCreate(self._handler, data)
        return self._backoffice_channel

        
    @property
    def active_products_channel(self):
        if not hasattr(self, "_active_products_channel"):
            data = self.request("%s%s/" % (self.resource_uri, 'active_products_channel'), method = "get")
            self._active_products_channel = UpdateableIcebergObject.findOrCreate(self._handler, data)
        return self._active_products_channel




class MerchantAddress(UpdateableIcebergObject):
    endpoint = 'merchant_address'

class StoreBankAccount(UpdateableIcebergObject):
    endpoint = 'store_bank_account'

class MerchantImage(IcebergObject):
    endpoint = 'merchant_image'

    def build_resized_image_url(self, width, height, process_mode="crop"):
        from icebergsdk.utils.image_server_utils import build_resized_image_url
        image_server_url = self._handler.conf.IMAGE_SERVER_URL
        return build_resized_image_url(image_server_url, self.image_path, width, height, process_mode)


class MerchantCommissionSettings(UpdateableIcebergObject):
    endpoint = 'commission_settings'


class MerchantShippingPolicy(UpdateableIcebergObject):
    endpoint = 'merchant_policy_parameter'


class MerchantFeed(UpdateableIcebergObject):
    endpoint = 'merchant_catalog_feed'

    def validate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'validate'), method = "post")
        return self._load_attributes_from_response(**data)

    def parse(self):
        return self.request("%s%s/" % (self.resource_uri, 'parse'), method = "post")


class MerchantTransaction(IcebergObject):
    endpoint = 'store_transaction'

