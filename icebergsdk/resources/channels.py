# -*- coding: utf-8 -*-
import time
from icebergsdk.resources.base import UpdateableIcebergObject, IcebergObject, IcebergObjectNotFound, IcebergMultipleObjectsReturned
import pytz
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging
logger = logging.getLogger('icebergsdk.resource')

class ProductChannelLogEvent(IcebergObject):
    endpoint = 'product_channel_log_event'


class ChannelPropagationPolicy(UpdateableIcebergObject):
    endpoint = 'product_channel_propagation_policy'


class ProductChannel(UpdateableIcebergObject):
    endpoint = 'product_channel'

    DATETIME_FIELDS = ["algolia_api_key_expiration_date",]

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
        

    def get_products(self, limit=20, offset=0):
        """
        Get products from channel storage
        """
        params = {
            'offset': offset,
            'limit': limit,
        }
        result = self.request("%s%s/" % (self.resource_uri, 'viewer'), method = "get", args=params)
        products = []
        for element in result:
            products.append(UpdateableIcebergObject.findOrCreate(self._handler, element))
        return products

    def get_product(self, product_id, raw_result=False):
        """
        Get product from channel storage
        """

        result = self.request("%s%s/%s/" % (self.resource_uri, 'viewer', product_id), method = "get")
        if len(result) > 1:
            raise IcebergMultipleObjectsReturned()
        elif len(result) == 0:
            raise IcebergObjectNotFound()
        if raw_result:
            return result[0]
        else:
            return UpdateableIcebergObject.findOrCreate(self._handler, result[0])

    def storage_wait_for_value(self, product_id, value_name, expected_value, max_wait=60, retry_every=5):
        """ 
        Returns True if 'value_name' equals 'expected_value' before 'max_wait' seconds else False
        """
        def get_value_from_path(data, path_to_value):
            for path_step in path_to_value.split("."):
                data = data.get(path_step,{})
            return data

        data = self.get_product(product_id, raw_result=True)
        timeout = time.time() + max_wait
        actual_value = get_value_from_path(data, value_name)
        while time.time() < timeout  and not actual_value == expected_value:
            logger.debug("Waiting %s seconds for value '%s' to change to '%s'" %
                (retry_every, value_name, expected_value)
            )
            time.sleep(retry_every)
            data = self.get_product(product_id, raw_result=True)
            actual_value = get_value_from_path(data, value_name)

        if actual_value == expected_value:
            return True
        else:
            logger.warn(
                u"Waited %s seconds, value '%s' is still '%s' (!=%s)" % 
                (max_wait, value_name, actual_value, expected_value)
            )
            return False

    @property
    def algolia_index(self):
        to_refetch = self.algolia_api_key_expiration_date < datetime.now(pytz.utc)+relativedelta(minutes=20)
        if to_refetch:
            self.fetch()
        if not hasattr(self, "_algolia_index") or to_refetch:
            try:
                from algoliasearch import algoliasearch
            except ImportError:
                raise Exception("Please install algoliasearch requirement")
            
            ## now returned by api
            # algolia_application_id = os.getenv('ALGOLIA_APPLICATION_ID', None)
            # if not algolia_application_id:
            #     raise Exception("Please define ALGOLIA_APPLICATION_ID environment variable")

            client = algoliasearch.Client(self.algolia_application_id, self.algolia_api_key)
            self._algolia_index = client.initIndex(self.algolia_index_name)

        return self._algolia_index


    def algolia_search(self, query, search_options=None):
        """
        algoliasearch wrapper (similar to Product.search)
        @return tuple   search result (products, meta)
        """
        from icebergsdk.resources import Product
        result = self.algolia_index.search(query, search_options)
        products = []
        for element in result.pop('hits',[]):
            products.append(Product.findOrCreate(self._handler, element))
        return products, result

    def algolia_fetch(self, product):
        data = self.algolia_index.get_object(product.id)
        return product._load_attributes_from_response(**data)

    def algolia_find(self, product_id, raw_result=False):
        from icebergsdk.resources import Product
        data = self.algolia_index.get_object(product_id)
        if raw_result:
            return data
        else:
            return Product.findOrCreate(self._handler, data)


    def algolia_wait_for_value(self, product_id, value_name, expected_value, max_wait=60, retry_every=5, process_function=None):
        """ 
        Returns True if 'value_name' equals 'expected_value' before 'max_wait' seconds else False
        """
        def get_value_from_path(data, path_to_value):
            for path_step in path_to_value.split("."):
                data = data.get(path_step,{})
            return process_function(data) if process_function else data

        data = self.algolia_find(product_id, raw_result=True)
        timeout = time.time() + max_wait
        actual_value = get_value_from_path(data, value_name)
        while time.time() < timeout  and not actual_value == expected_value:
            logger.debug("Waiting %s seconds for value '%s' to change to '%s'" %
                (retry_every, value_name, expected_value)
            )
            time.sleep(retry_every)
            data = self.algolia_find(product_id, raw_result=True)
            actual_value = get_value_from_path(data, value_name)

        if actual_value == expected_value:
            return True
        else:
            logger.warn(
                u"Waited %s seconds, value '%s' is still '%s' (!=%s)" % 
                (max_wait, value_name, actual_value, expected_value)
            )
            return False