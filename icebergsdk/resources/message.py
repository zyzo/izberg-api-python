# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Message(UpdateableIcebergObject):
    endpoint = 'message'

    def read(self):
        """
        Mark message as read
        """
        data = self.request("%s%s/" % (self.resource_uri, 'read'), method = "post")
        return self._load_attributes_from_response(**data)

    def close(self):
        """
        Mark message as read
        """
        data = self.request("%s%s/" % (self.resource_uri, 'close'), method = "post")
        return self._load_attributes_from_response(**data)




