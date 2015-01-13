# -*- coding: utf-8 -*-
import os
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
        self.request("%s%s/" % (self.resource_uri, 'trigger'), method = "post", post_args=event_dict)
        


    @property
    def algolia_index(self):
        if not hasattr(self, "_algolia_index"):
            try:
                from algoliasearch import algoliasearch
            except ImportError:
                raise Exception("Please install algoliasearch requirement")
            
            algolia_application_id = os.getenv('ALGOLIA_APPLICATION_ID', None)

            if not algolia_application_id:
                raise Exception("Please define ALGOLIA_APPLICATION_ID environment variable")

            client = algoliasearch.Client(algolia_application_id, self.algolia_api_key)
            self._algolia_index = client.initIndex(self.algolia_index_name)

        return self._algolia_index


    def algolia_search(self, query):
        from icebergsdk.resources import Product
        result = self.algolia_index.search(query)
        products = []
        for element in result.pop('hits',[]):
            products.append(Product.findOrCreate(self._handler, element))
        return products, result

