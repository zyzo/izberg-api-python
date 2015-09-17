# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject


class ServiceOfferVariation(UpdateableIcebergObject):
    endpoint = 'service_offer_variation'


class ServiceOffer(UpdateableIcebergObject):
    endpoint = 'service_offer'

    def activate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'activate'), method="post")
        return self._load_attributes_from_response(**data)

    def deactivate(self):
        data = self.request("%s%s/" % (self.resource_uri, 'deactivate'), method="post")
        return self._load_attributes_from_response(**data)


class ServiceOption(UpdateableIcebergObject):
    endpoint = 'service_option'
