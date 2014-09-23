# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject

class Webhook(UpdateableIcebergObject):
    endpoint = 'webhook'

    def test_trigger(self):
        data = self.request("%s%s/" % (self.resource_uri, 'test_trigger'), method = "post")
        return data

    def triggers(self):
        return self.get_list('%striggers/' % self.resource_uri)


    def get_test_endpoint_url(self):
        return "%s/%s/" % ("/".join(self.resource_uri.split("/")[:-2]), 'test_endpoint')


class WebhookTrigger(IcebergObject):
    endpoint = 'webhook_trigger'

    def attempts(self):
        return self.get_list('%sattempts/' % self.resource_uri)


class WebhookTriggerAttempt(IcebergObject):
    endpoint = 'webhook_trigger_attempt'
