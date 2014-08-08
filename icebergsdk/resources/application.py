# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject

class Application(IcebergObject):
    endpoint = 'application'

    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)
