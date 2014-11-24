# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject, IcebergObject


class Application(UpdateableIcebergObject):
    endpoint = 'application'

    # Messages
    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def outbox(self):
        return self.get_list("%soutbox/" % self.resource_uri)

    def merchants(self, params = None):
        params = params or {}
        return self.get_list("%smerchants/" % self.resource_uri, args = params)

    def fetch_secret_key(self):
    	return self.request("%sfetchSecretKey/" % self.resource_uri)["secret_key"]

    def auth_me(self):
        """
        Return the access_token for the current user on this application
        """
        return self.request("%sauth_me/" % self.resource_uri)["access_token"]




class ApplicationCommissionSettings(UpdateableIcebergObject):
    endpoint = 'application_commission_settings'

class ApplicationPaymentSettings(UpdateableIcebergObject):
    endpoint = 'app_payment_settings'



class ApplicationUrls(UpdateableIcebergObject):
    endpoint = 'application_urls'



class ApplicationMerchantPolicies(UpdateableIcebergObject):
    endpoint = 'application_merchant_policies'



    def set_mandatory_fields(self, payment_card=None, products=None, 
                                   return_info=None, shipping_info=None, 
                                   store_contact=None, store_information=None,
                                   store_legal=None):
        if not hasattr(self, "mandatory_info"):
            self.mandatory_info = {}

        if payment_card is not None:
            self.mandatory_info["payment_card"] = payment_card
        if products is not None:
            self.mandatory_info["products"] = products
        if return_info is not None:
            self.mandatory_info["return_info"] = return_info
        if shipping_info is not None:
            self.mandatory_info["shipping_info"] = shipping_info
        if store_contact is not None:
            self.mandatory_info["store_contact"] = store_contact
        if store_information is not None:
            self.mandatory_info["store_information"] = store_information
        if store_legal is not None:
            self.mandatory_info["store_legal"] = store_legal

        self.save()


class ApplicationTransaction(IcebergObject):
    endpoint = 'app_transaction'

    
