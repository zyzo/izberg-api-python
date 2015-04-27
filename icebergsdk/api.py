# -*- coding: utf-8 -*-

import mimetypes
import logging
import time
import hashlib
import hmac
import datetime

from icebergsdk.exceptions import IcebergMissingApplicationSettingsError
from icebergsdk.exceptions import IcebergMissingSsoData

from icebergsdk import resources
from icebergsdk.managers import ResourceManager, UserResourceManager, CartResourceManager, StoreResourceManager
from icebergsdk.mixins.request_mixin import IcebergRequestBase

logger = logging.getLogger('icebergsdk')


class IcebergAPI(IcebergRequestBase):

    def __init__(self, *args, **kwargs):
        super(IcebergAPI, self).__init__(*args, **kwargs)

        self.define_resources()  # Resources definition
        self._objects_store = {}  # Will store the object for relationship management

    def define_resources(self):
        """
        For faster initialization, set the handler in the resources classes
        """
        resource_classes_list = [
            resources.Application,
            resources.ApplicationCommissionSettings,
            resources.ApplicationPaymentSettings,
            resources.ApplicationPermission,
            resources.ApplicationMerchantPolicies,
            resources.ApplicationTransaction,
            resources.ApplicationUrls,
            resources.Address,
            resources.Brand,
            resources.ChannelPropagationPolicy,
            resources.Country,
            resources.Category,
            resources.MarketPlaceTransaction,
            resources.MerchantAddress,
            resources.MerchantCommissionSettings,
            resources.MerchantOrder,
            resources.MerchantFeed,
            resources.MerchantShippingPolicy,
            resources.MerchantTransaction,
            resources.Message,
            resources.MerchantReview,
            resources.Order,
            resources.UserShoppingPreference,
            resources.Review,
            resources.Return,
            resources.Refund,
            resources.StoreBankAccount,
            resources.Transaction,
            resources.ProductChannel,
            resources.ProductChannelLogEvent,
            resources.ProductVariation,
            resources.ProductOffer,
            resources.ProductOfferImage,
            resources.Product,
            resources.Profile,
            resources.Payment,
            resources.Permission,
            resources.ProductFamily,
            resources.ProductFamilySelector,
            resources.Webhook,
            resources.WebhookTrigger,
            resources.WebhookTrigger,
            resources.WebhookTriggerAttempt,
        ]

        for resource_class in resource_classes_list:
            setattr(self, resource_class.__name__, ResourceManager(resource_class=resource_class, api_handler=self))

        self.Cart = CartResourceManager(resource_class=resources.Cart, api_handler=self)
        self.User = UserResourceManager(resource_class=resources.User, api_handler=self)
        self.Store = StoreResourceManager(resource_class=resources.Store, api_handler=self)

        # Missing

        # Return
        # Store Reviews
        # Product Reviews
        # Invoices
        # Currencies
        # Webhooks
        # Feed Management

    def auth_user(self, username, email, first_name='', last_name='', is_staff=False, is_superuser=False):
        """
        Method for Iceberg Staff to get or create a user into the platform and get the access_token .

        For authentication, please use the SSO method.
        """
        if not self.conf.ICEBERG_API_PRIVATE_KEY:
            raise IcebergMissingApplicationSettingsError()

        timestamp = int(time.time())
        secret_key = str(self.conf.ICEBERG_API_PRIVATE_KEY)

        to_compose = [username, email, first_name or '', last_name or '', is_staff, is_superuser, timestamp]

        to_compose_str = []
        for elem in to_compose:
            if type(elem) == unicode:
                to_compose_str.append(elem.encode('utf-8'))
            else:
                to_compose_str.append(str(elem))

        hash_obj = hmac.new(b"%s" % secret_key, b";".join(to_compose_str), digestmod=hashlib.sha1)  # Expect strings
        message_auth = hash_obj.hexdigest()

        data = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'timestamp': timestamp,
            'message_auth': message_auth
        }

        response = self.request('user/auth/', args=data)

        self.username = response['username']
        self.access_token = response['access_token']

        self._auth_response = response

        return self

    def generate_messages_auth(self, data):
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        timestamp = data['timestamp']

        secret_key = str(self.conf.ICEBERG_APPLICATION_SECRET_KEY)

        to_compose = [email, first_name or "", last_name or "", str(timestamp)]

        if data.get('currency', None):
            to_compose.append(data.get('currency'))

        if data.get('shipping_country', None):
            to_compose.append(data.get('shipping_country'))

        if data.get('from_session_id', None):
            to_compose.append(str(data.get('from_session_id')))

        if data.get('birth_date', None):
            to_compose.append(data.get('birth_date'))

        to_compose_str = []
        for elem in to_compose:
            if type(elem) == unicode:
                to_compose_str.append(elem.encode('utf-8'))
            else:
                to_compose_str.append(str(elem))

        to_compose_str = ";".join(to_compose_str)

        logger.debug("Create message_auth with %s", to_compose_str)

        hash_obj = hmac.new(b"%s" % secret_key, b"%s" % to_compose_str, digestmod=hashlib.sha1)
        message_auth = hash_obj.hexdigest()
        return message_auth

    # def sso(self, email, first_name, last_name):
    def sso(self, email, first_name, last_name):
        """
        Depreciated
        """
        if not self.conf.ICEBERG_APPLICATION_NAMESPACE or not self.conf.ICEBERG_APPLICATION_SECRET_KEY:
            raise IcebergMissingApplicationSettingsError()

        timestamp = int(time.time())

        data = {
            'application': self.conf.ICEBERG_APPLICATION_NAMESPACE,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'timestamp': timestamp,
            'message_auth': self.generate_messages_auth({
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'timestamp': timestamp
            })
        }

        response = self.request('user/sso/', args=data)

        self.username = response['username']
        self.access_token = response['access_token']

        return response

    def sso_user(self, email=None, first_name=None, last_name=None, currency="EUR", shipping_country="FR", birth_date=None, include_application_data=True, from_session_id=None):
        if not self.conf.ICEBERG_APPLICATION_NAMESPACE or not self.conf.ICEBERG_APPLICATION_SECRET_KEY:
            raise IcebergMissingApplicationSettingsError(self.conf.ICEBERG_ENV)

        logger.debug("sso_user %s on application %s" % (email, self.conf.ICEBERG_APPLICATION_NAMESPACE))
        timestamp = int(time.time())

        if birth_date and isinstance(birth_date, datetime.date):
            birth_date = birth_date.isoformat()

        data = {
            'application': self.conf.ICEBERG_APPLICATION_NAMESPACE,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'timestamp': timestamp,
            'from_session_id': from_session_id,
            'include_application_data': include_application_data,
            'message_auth': self.generate_messages_auth({
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'timestamp': timestamp,
                'currency': currency,
                'from_session_id': from_session_id,
                'shipping_country': shipping_country,
                'birth_date': birth_date
            })
        }

        if shipping_country:
            data['shipping_country'] = shipping_country

        if currency:
            data['currency'] = currency

        if birth_date:
            data['birth_date'] = birth_date

        response = self.request('user/sso/', args=data)

        self.username = response['username']
        self.access_token = response['access_token']

        self._auth_response = response

        return self
        # return response

    def _sso_response():
        doc = "For compatibility matter, but now, should use _auth_response."

        def fget(self):
            return self._auth_response

        def fset(self, value):
            self._auth_response = value

        def fdel(self):
            del self._auth_response
        return locals()
    _sso_response = property(**_sso_response())

    def send_image(self, path, image_path, method="post"):
        mimetype, encoding = mimetypes.guess_type(image_path)
        image_name = image_path.split("/")[-1]
        image_info = ('image', (image_name, open(image_path, 'rb'), mimetype))
        headers = {
            'Accept-Language': self.lang,
            'Authorization': self.get_auth_token()
        }
        return self.request(path, files=[image_info], method=method, headers=headers)

    def get_element(self, resource, object_id):
        return self.request("%s/%s/" % (resource, object_id))

    def get_list(self, path, **kwargs):
        if not path.endswith('/'):
            path = "%s/" % path

        result = self.request(path, **kwargs)
        return result['objects']

    def convert_to_register_user(self):
        raise NotImplementedError()

    def me(self):
        """
        Return User resource
        """
        if not hasattr(self, '_auth_response'):
            raise IcebergMissingSsoData()

        return self.User.findOrCreate(self._auth_response)

    #####
    #
    # Shortcuts..  Will be removed
    #
    #####
    # User
    def get_me(self):
        return self.request("user/me/")

    # Cart
    def get_my_cart(self):
        return self.request("cart/mine/")

    # Merchants
    def get_my_merchants(self):
        return self.get_list('merchant')

    def get_merchant(self, object_id):
        return self.get_element('merchant', object_id)

    # Applications
    def get_my_applications(self):
        return self.get_list('application')

    def get_application(self, object_id):
        return self.get_element('application', object_id)
