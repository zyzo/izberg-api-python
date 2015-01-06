# -*- coding: utf-8 -*-
import mimetypes
import logging, requests, json, time, hashlib, hmac

from icebergsdk.exceptions import IcebergAPIError, IcebergServerError, IcebergClientError
from icebergsdk.exceptions import IcebergClientUnauthorizedError, IcebergMissingApplicationSettingsError
from icebergsdk.exceptions import IcebergMissingSsoData

from icebergsdk.conf import Configuration
from icebergsdk import resources
from icebergsdk.managers import ResourceManager, UserResourceManager, CartResourceManager
from icebergsdk.json_utils import DateTimeAwareJSONEncoder

logger = logging.getLogger('icebergsdk')

class IcebergAPI(object):
    def __init__(self, username = None, access_token = None, lang = None, timeout = None, conf = None):
        """
        @conf:
            Configuration, ConfigurationSandbox or custom conf
        """
        # Conf
        self.conf = conf or Configuration
        self.username = username
        self.access_token = access_token
        self.timeout = timeout
        self.lang = lang or self.conf.ICEBERG_DEFAULT_LANG
        self.define_resources() # Resources definition
        self._objects_store = {} # Will store the object for relationship management


    def define_resources(self):
        """
        For faster initialization, set the handler in the resources classes
        """
        self.Application = ResourceManager(resource_class=resources.Application, api_handler=self)
        self.ApplicationCommissionSettings = ResourceManager(resource_class=resources.ApplicationCommissionSettings, api_handler=self)
        self.ApplicationPaymentSettings = ResourceManager(resource_class=resources.ApplicationPaymentSettings, api_handler=self)
        self.ApplicationMerchantPolicies = ResourceManager(resource_class=resources.ApplicationMerchantPolicies, api_handler=self)
        self.ApplicationTransaction = ResourceManager(resource_class=resources.ApplicationTransaction, api_handler=self)
        self.ApplicationUrls = ResourceManager(resource_class=resources.ApplicationUrls, api_handler=self)
        self.MarketPlaceTransaction = ResourceManager(resource_class=resources.MarketPlaceTransaction, api_handler=self)
        self.Address = ResourceManager(resource_class=resources.Address, api_handler=self)
        self.Cart = CartResourceManager(resource_class=resources.Cart, api_handler=self)
        self.Country = ResourceManager(resource_class=resources.Country, api_handler=self)
        self.MerchantOrder = ResourceManager(resource_class=resources.MerchantOrder, api_handler=self)
        self.Order = ResourceManager(resource_class=resources.Order, api_handler=self)
        self.ProductVariation = ResourceManager(resource_class=resources.ProductVariation, api_handler=self)
        self.ProductOffer = ResourceManager(resource_class=resources.ProductOffer, api_handler=self)
        self.ProductOfferImage = ResourceManager(resource_class=resources.ProductOfferImage, api_handler=self)
        self.Product = ResourceManager(resource_class=resources.Product, api_handler=self)
        self.Profile = ResourceManager(resource_class=resources.Profile, api_handler=self)
        self.Payment = ResourceManager(resource_class=resources.Payment, api_handler=self)

        self.Store = ResourceManager(resource_class=resources.Store, api_handler=self)
        self.StoreBankAccount = ResourceManager(resource_class=resources.StoreBankAccount, api_handler=self)
        self.MerchantAddress = ResourceManager(resource_class=resources.MerchantAddress, api_handler=self)
        self.MerchantCommissionSettings = ResourceManager(resource_class=resources.MerchantCommissionSettings, api_handler=self)
        self.MerchantFeed = ResourceManager(resource_class=resources.MerchantFeed, api_handler=self)
        self.MerchantShippingPolicy = ResourceManager(resource_class=resources.MerchantShippingPolicy, api_handler=self)
        self.MerchantTransaction = ResourceManager(resource_class=resources.MerchantTransaction, api_handler=self)
        
        self.User = UserResourceManager(resource_class=resources.User, api_handler=self)
        self.Message = ResourceManager(resource_class=resources.Message, api_handler=self)
        self.Review = ResourceManager(resource_class=resources.Review, api_handler=self)
        self.MerchantReview = ResourceManager(resource_class=resources.MerchantReview, api_handler=self)
        self.UserShoppingPreference = ResourceManager(resource_class=resources.UserShoppingPreference, api_handler=self)
        self.Category = ResourceManager(resource_class=resources.Category, api_handler=self)
        self.Brand = ResourceManager(resource_class=resources.Brand, api_handler=self)

        self.Webhook = ResourceManager(resource_class=resources.Webhook, api_handler=self)
        self.WebhookTrigger = ResourceManager(resource_class=resources.WebhookTrigger, api_handler=self)
        self.WebhookTrigger = ResourceManager(resource_class=resources.WebhookTrigger, api_handler=self)
        self.WebhookTriggerAttempt = ResourceManager(resource_class=resources.WebhookTriggerAttempt, api_handler=self)

        
        self.Transaction = ResourceManager(resource_class=resources.Transaction, api_handler=self)

        self.Return = ResourceManager(resource_class=resources.Return, api_handler=self)
        self.Refund = ResourceManager(resource_class=resources.Refund, api_handler=self)
        
        ### Missing

        # Return
        # Store Reviews
        # Product Reviews
        # Invoices
        # Currencies
        # Webhooks
        # Feed Management


    def get_auth_token(self):
        if self.username == "Anonymous":
            return '%s %s:%s:%s' % (self.conf.ICEBERG_AUTH_HEADER, self.username, self.conf.ICEBERG_APPLICATION_NAMESPACE, self.access_token)
        else:
            return '%s %s:%s' % (self.conf.ICEBERG_AUTH_HEADER, self.username, self.access_token)

    def auth_user(self, username, email, first_name = '', last_name = '', is_staff = False, is_superuser = False):
        """
        Method for Iceberg Staff to get or create a user into the platform and get the access_token .

        For authentication, please use the SSO method.
        """
        if not self.conf.ICEBERG_API_PRIVATE_KEY:
            raise IcebergMissingApplicationSettingsError()

        timestamp = int(time.time())
        secret_key = self.conf.ICEBERG_API_PRIVATE_KEY

        to_compose = [username, email, first_name, last_name, is_staff, is_superuser, timestamp]
        hash_obj = hmac.new(b"%s" % secret_key, b";".join(str(x) for x in to_compose), digestmod = hashlib.sha1)
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

        response = self.request('user/auth/', args = data)

        self.username = username
        self.access_token = response['access_token']

        self._auth_response = response

        return self

    def generate_messages_auth(self, data):
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        timestamp = data['timestamp']

        
        secret_key = self.conf.ICEBERG_APPLICATION_SECRET_KEY

        to_compose = [email, first_name, last_name, timestamp]
        hash_obj = hmac.new(b"%s" % secret_key, b";".join(str(x) for x in to_compose), digestmod = hashlib.sha1)
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

        response = self.request('user/sso/', args = data)

        self.username = response['username']
        self.access_token = response['access_token']

        return response


    def sso_user(self, email = None, first_name = None, last_name = None, currency = "EUR", shipping_country = "FR", include_application_data = True):
        if not self.conf.ICEBERG_APPLICATION_NAMESPACE or not self.conf.ICEBERG_APPLICATION_SECRET_KEY:
            raise IcebergMissingApplicationSettingsError()

        print "sso_user %s on application %s" % (email, self.conf.ICEBERG_APPLICATION_NAMESPACE)
        timestamp = int(time.time())

        data = {
            'application': self.conf.ICEBERG_APPLICATION_NAMESPACE,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'timestamp': timestamp,
            'include_application_data': include_application_data,
            'message_auth': self.generate_messages_auth({
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'timestamp': timestamp,
                'currency': currency,
                'shipping_country': shipping_country
            })
        }

        response = self.request('user/sso/', args = data)

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



    def request(self, path, args = None, post_args = None, files = None, method = None, headers = None):
        args = args or {}
        method = method or "GET"

        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Accept-Language': self.lang,
                'Authorization': self.get_auth_token()
            }
        # store = requests.get('http://api.local.iceberg-marketplace.com:8000/v1/merchant/', params = {'slug': store_slug}, headers = headers)

        if '//' not in path:
            url = "%s:%s/" % (self.conf.ICEBERG_API_URL, self.conf.ICEBERG_API_PORT)

            if not self.conf.ICEBERG_API_VERSION in path:
                url = "%s%s/" % (url, self.conf.ICEBERG_API_VERSION)

            if path.startswith('/'):
                url = url[:-1] # Remove /
        else:
            url = ""

        url += path

        # HAcK to fix missing server conf. Will be remove soon
        if getattr(self.conf, 'ICEBERG_ENV', "prod") == "sandbox":
            url = url.replace('https://api.iceberg', 'http://api.sandbox.iceberg')
        # End Hack

        logger.debug('REQUEST %s - %s - %s - GET PARAMS: %s - POST PARAMS: %s', method, url, headers, args, post_args)
        try:
            if post_args:
                post_args = json.dumps(post_args, cls=DateTimeAwareJSONEncoder, ensure_ascii=False)

            response = requests.request(method,
                                        url,
                                        timeout=self.timeout,
                                        params=args,
                                        data=post_args,
                                        files=files,
                                        headers=headers)
        except requests.HTTPError as e:
            response = json.loads(e.read())
            raise IcebergAPIError(response)

        try:
            try:
                elapsed = response.elapsed.total_seconds()
            except:
                elapsed = (response.elapsed.days * 1440 + response.elapsed.seconds // 60)*60
            logger.debug('RESPONSE - Status: %s - Response Time (s): %s - %s', response.status_code, elapsed, response.text)
        except Exception:
            logger.exception('ERROR in response printing')

        if response.status_code == 401:
            raise IcebergClientUnauthorizedError()
            
        elif 400 <= response.status_code < 500:
            raise IcebergClientError(response, url = url)

        elif 500 <= response.status_code <= 600:
            raise IcebergServerError(response)
        
        if response.content:
            return response.json()
        else:
            return "No Content"


    def send_image(self, path, image_path, method="post"):
        mimetype, encoding = mimetypes.guess_type(image_path)
        image_name = image_path.split("/")[-1]
        image_info = ('image', (image_name, open(image_path, 'rb'), mimetype) )
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



