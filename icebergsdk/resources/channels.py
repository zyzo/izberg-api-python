# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class ProductChannel(UpdateableIcebergObject):
    endpoint = 'product_channel'

    def full_sync(self):
        """
        Ask for full_sync
        """
        event_dict = {
            "event":"full_sync"
        }
        return self.trigger_event(event_dict)

    def trigger_event(self, event_dict):
        """
        Trigger an event in channel
        """
        data = self.request("%s%s/" % (self.resource_uri, 'trigger'), method = "post", post_args=event_dict)
        return self._load_attributes_from_response(**data)




