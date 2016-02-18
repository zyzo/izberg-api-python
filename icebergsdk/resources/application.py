# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject, IcebergObject


class Application(UpdateableIcebergObject):
    endpoint = 'application'

    # Messages
    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def outbox(self):
        return self.get_list("%soutbox/" % self.resource_uri)

    def merchants(self, params = None):
        params = params or {}
        return self.get_list("%smerchants/" % self.resource_uri, args = params)

    def linked_merchants(self, params = None):
        params = params or {}
        return self.get_list("%slinked_merchants/" % self.resource_uri, args = params)

    def created_merchants(self, params = None):
        params = params or {}
        return self.get_list("%screated_merchants/" % self.resource_uri, args = params)

    def fetch_secret_key(self):
        return self.request("%sfetchSecretKey/" % self.resource_uri)["secret_key"]

    def auth_me(self):
        """
        Return the access_token for the current user on this application
        """
        return self.request("%sauth_me/" % self.resource_uri)["access_token"]


    def product_channels(self, params = None, limit = None, offset = 0):
        params = params or {}
        return self.get_list("%sproduct_channels/" % self.resource_uri, args = params)


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

    def filter_channels(self, data, language, fallback, fallback_language):
            res = []
            fallback_channel = []
            for channel in data['objects']:
                if channel['language'] == language:
                    res.append(channel)
                elif fallback and channel['language'] == fallback_language:
                    fallback_channel.append(channel)
            return res if res else fallback_channel

    def get_active_products_channel(self, language=None, fallback=True, fallback_language='en'):
        cache_key = '_active_products_channel_%s_%s' % (language, fallback)
        if not hasattr(self, cache_key):
            url = "%s%s/" % (self.resource_uri, 'active_products_channels')
            if language and not fallback:
                url += '?language=%s' % language
            data = self.request(url, method="get")
            data.update({
                'objects': self.filter_channels(data, language, fallback, fallback_language)
            })
            if data['meta']['total_count']:
                channel = UpdateableIcebergObject.findOrCreate(self._handler, data['objects'][0])
                setattr(self, cache_key, channel)
        return getattr(self, cache_key)

    def get_active_products_channels(self, language=None, fallback=True, fallback_language='en'):
        cache_key = '_active_products_channels_%s_%s' % (language, fallback)
        if not hasattr(self, cache_key) or 1 == 1:
            url = "%s%s/" % (self.resource_uri, 'active_products_channels')
            if language and not fallback:
                url += '?language=%s' % language
            data = self.request(url, method="get")
            data.update({
                'objects': self.filter_channels(data, language, fallback, fallback_language)
            })
            channels = UpdateableIcebergObject.findOrCreate(self._handler, data)
            setattr(self, cache_key, channels)
        return getattr(self, cache_key)


class ApplicationCommissionSettings(UpdateableIcebergObject):
    endpoint = 'application_commission_settings'

class ApplicationPaymentSettings(UpdateableIcebergObject):
    endpoint = 'app_payment_settings'


class ApplicationPermission(UpdateableIcebergObject):
    endpoint = 'app_permission'


class ApplicationUrls(UpdateableIcebergObject):
    endpoint = 'application_urls'



class ApplicationMerchantPolicies(UpdateableIcebergObject):
    endpoint = 'application_merchant_policies'



    def set_mandatory_fields(self, payment_card=None, products=None, 
                                   return_info=None, shipping_info=None, 
                                   store_contact=None, store_information=None,
                                   store_legal=None):
        if not hasattr(self, "mandatory_info"):
            self.mandatory_info = {}

        if payment_card is not None:
            self.mandatory_info["payment_card"] = payment_card
        if products is not None:
            self.mandatory_info["products"] = products
        if return_info is not None:
            self.mandatory_info["return_info"] = return_info
        if shipping_info is not None:
            self.mandatory_info["shipping_info"] = shipping_info
        if store_contact is not None:
            self.mandatory_info["store_contact"] = store_contact
        if store_information is not None:
            self.mandatory_info["store_information"] = store_information
        if store_legal is not None:
            self.mandatory_info["store_legal"] = store_legal

        self.save()


class ApplicationTransaction(IcebergObject):
    endpoint = 'app_transaction'

    
