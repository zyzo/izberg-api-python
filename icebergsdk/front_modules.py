# -*- coding: utf-8 -*-
import logging

from icebergsdk.mixins.request_mixin import IcebergRequestBase

logger = logging.getLogger('icebergsdk.frontmodules')

class FrontModules(IcebergRequestBase):
    cache_key = "icebergsdk:frontmodule:data"
    cache_expire = 60*60 # one hour

    def __init__(self, *args, **kwargs):
        super(FrontModules, self).__init__(*args, **kwargs)
        self.cache = kwargs.get('cache', None)
        self.lang = kwargs.get('lang', "en")
        self.debug = kwargs.get('debug', False)


    def get_module_data(self, module_name):
        return self.modules_data['modules'][module_name]

    ####
    #   Loader
    ####
    @property
    def modules_data(self):
        """
        Helper to fetch Iceberg client side javascript templates
        """
        if hasattr(self, "_modules_data_%s" % self.lang):
            return getattr(self, "_modules_data_%s" % self.lang)

        if self.cache:
            data = self.cache.get("%s:%s" % (self.cache_key, self.lang), False)
            if data:
                setattr(self, '_modules_data_%s' % self.lang, data)
                return data

        data = self.request(self.conf.ICEBERG_MODULES_URL, args = {
            "lang": self.lang,
            "enviro": self.conf.ICEBERG_ENV,
            "debug": self.debug
        }) # Do to, add lang
        setattr(self, '_modules_data_%s' % self.lang, data)
        if self.cache:
            self.cache.set("%s:%s" % (self.cache_key, self.lang), data, self.cache_expire)

        return data


