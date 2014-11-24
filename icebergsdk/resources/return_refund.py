# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Return(UpdateableIcebergObject):
    endpoint = 'return'

    def accept(self):
        data = self.request("%s%s/" % (self.resource_uri, 'accept'), method = "post")
        return self._load_attributes_from_response(**data)

    def received(self):
        data = self.request("%s%s/" % (self.resource_uri, 'received'), method = "post")
        return self._load_attributes_from_response(**data)

    def cancel(self):
        data = self.request("%s%s/" % (self.resource_uri, 'cancel'), method = "post")
        return self._load_attributes_from_response(**data)

    def close(self):
        data = self.request("%s%s/" % (self.resource_uri, 'close'), method = "post")
        return self._load_attributes_from_response(**data)

    def seller_close(self):
        data = self.request("%s%s/" % (self.resource_uri, 'seller_close'), method = "post")
        return self._load_attributes_from_response(**data)
    
    def reopen(self):
        data = self.request("%s%s/" % (self.resource_uri, 'reopen'), method = "post")
        return self._load_attributes_from_response(**data)

    def get_merchant_order(self):
        data = self.request("%s%s/" % (self.resource_uri, 'get_merchant_order'), method = "get")
        return self._load_attributes_from_response(**data)



class Refund(UpdateableIcebergObject):
    endpoint = 'refund'

    def cancel(self):
        data = self.request("%s%s/" % (self.resource_uri, 'cancel'), method = "post")
        return self._load_attributes_from_response(**data)
