# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Store(UpdateableIcebergObject):
    endpoint = 'merchant'
    
    def product_offers(self):
        return self.get_list('productoffer', args = {'merchant': self.id})

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)


    def import_products(self):
        """
        Return product from XML file
        Use for initial import
        """
        feed_url = "%sdownload_export/" % self.resource_uri

        from icebergsdk.parser import XMLParser

        parser = XMLParser()

        res = []
        for element in parser.parse_feed(feed_url):
            res.append(UpdateableIcebergObject.findOrCreate(element))

        return res

