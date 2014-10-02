# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject
import time

class Webhook(UpdateableIcebergObject):
    endpoint = 'webhook'

    def test_trigger(self):
        data = self.request("%s%s/" % (self.resource_uri, 'test_trigger'), method = "post")
        return data

    def triggers(self, **filters):
        return self.get_list('%striggers/' % self.resource_uri, args=filters)


    def get_test_endpoint_url(self):
        return "%s/%s/" % ("/".join(self.resource_uri.split("/")[:-2]), 'test_endpoint')


    def wait_for_triggers(self, number_of_triggers_expected=1, max_number_of_checks=10, check_every_seconds=5):
        webhook_triggers = []
        ## looping to wait for the webhook to be triggered
        number_of_attempts = 0
        while number_of_attempts<max_number_of_checks and len(webhook_triggers)<number_of_triggers_expected:
            if number_of_attempts > 0:
                time.sleep(check_every_seconds) ## check every X seconds except the 1st time
            webhook_triggers = self.triggers(status="succeeded")
            number_of_attempts += 1
        print "number_of_attempts = %s, webhook_triggers=%s" % (number_of_attempts, webhook_triggers)
        return webhook_triggers

class WebhookTrigger(IcebergObject):
    endpoint = 'webhook_trigger'

    def attempts(self, **filters):
        return self.get_list('%sattempts/' % self.resource_uri, args=filters)


class WebhookTriggerAttempt(IcebergObject):
    endpoint = 'webhook_trigger_attempt'
