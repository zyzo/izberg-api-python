# -*- coding: utf-8 -*-
import logging

from icebergsdk.mixins.request_mixin import IcebergRequestBase

logger = logging.getLogger('icebergsdk.frontmodules')


class FrontModules(IcebergRequestBase):
    cache_expire = 60 * 20  # 20 minutes

    def __init__(self, *args, **kwargs):
        super(FrontModules, self).__init__(*args, **kwargs)
        self.cache = kwargs.get('cache', None)
        self.lang = kwargs.get('lang', "en")
        self.debug = kwargs.get('debug', False)
        self.module_debug = kwargs.get('module_debug', self.debug)

    def get_module_data(self, module_name):
        return self.modules_data['modules'][module_name]

    ####
    #   Loader
    ####
    @property
    def cache_key(self):
        return "icebergsdk:frontmodule:data:%s:%s:%s" % (
            self.lang,
            self.conf.ICEBERG_ENV,
            self.debug,
        )

    @property
    def modules_data(self):
        """
        Helper to fetch Iceberg client side javascript templates
        """
        # if hasattr(self, "_modules_data_%s" % self.lang):
        #     return getattr(self, "_modules_data_%s" % self.lang)

        if self.cache:
            data = self.cache.get(self.cache_key, False)
            if data:
                # setattr(self, '_modules_data_%s' % self.lang, data)
                return data

        data = self.request(self.conf.ICEBERG_MODULES_URL, args={
            "lang": self.lang,
            "enviro": self.conf.ICEBERG_ENV,
            "debug": self.module_debug
        })  # Do to, add lang
        # setattr(self, '_modules_data_%s' % self.lang, data)
        if self.cache:
            self.cache.set(self.cache_key, data, self.cache_expire)

        return data
