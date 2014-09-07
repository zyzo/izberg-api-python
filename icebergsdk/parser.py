# -*- coding: utf-8 -*-

import urllib2, logging

logger = logging.getLogger('icebergsdk')


class XMLParser(object):
    path_to_products = "products.product"

    def parse_feed(self, feed_url):
        products = []

        try:
            file_down = urllib2.urlopen(feed_url, timeout=180)
        except urllib2.URLError, err:
            logger.error(err.reason)
        except urllib2.HTTPError, err:
            logger.error(err.reason)                        
        else:
            products = self.parse_file(file_down)

        # Close file
        try:
            file_down.close() # For sure, the two others maybe not
        except:
            pass

        return products

    def parse_file(self, the_file):
        """
        XML parsing using etree
        """
        from lxml import etree

        content = the_file.read()

        self.raw_dict = self.etree_to_dict(etree.fromstring(content).find("."))

        print self.raw_dict

        self.products_list = self.raw_dict
        for path in self.path_to_products.split("."):
            logger.debug("self.products_list keys=%s path=%s" % (self.products_list.keys(), path))
            self.products_list = self.products_list.get(path, {})

        return self.products_list


    def etree_to_dict(self, t):
        from collections import defaultdict
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self. etree_to_dict, children):
                for k, v in dc.iteritems():
                    dd[k].append(v)
            # try:
            #     d = { t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()} }
            # except SyntaxError:
            # logger.warn("d = { t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()} } SyntaxError")
            if not d.has_key(t.tag) or d[t.tag] == None:
                d[t.tag] = {}

            for k, v in dd.iteritems():
                if len(v) == 1:
                    d[t.tag][k] = v[0]
                else:
                    d[t.tag][k] = v 
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d






