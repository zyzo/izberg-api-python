# -*- coding: utf-8 -*-

import logging, requests, json

from icebergsdk.conf import Configuration
from icebergsdk.exceptions import IcebergError, IcebergAPIError, IcebergServerError, IcebergClientError
from icebergsdk.exceptions import IcebergClientUnauthorizedError, IcebergObjectNotFound

from icebergsdk.json_utils import DateTimeAwareJSONEncoder

logger = logging.getLogger('icebergsdk.request')

class IcebergRequestBase(object):
    """
    Utils mixin to deal with API requests
    """
    def __init__(self, *args, **kwargs):
        """
        @conf:
            Configuration, ConfigurationSandbox or custom conf
        """
        self.conf = kwargs.get('conf', Configuration)
        self.username = kwargs.get('username', None)
        self.access_token = kwargs.get('access_token', None)
        self.timeout = kwargs.get('timeout', None)
        self.lang = kwargs.get('lang', self.conf.ICEBERG_DEFAULT_LANG)


    def get_auth_token(self):
        if self.username == "Anonymous":
            return '%s %s:%s:%s' % (self.conf.ICEBERG_AUTH_HEADER, self.username, self.conf.ICEBERG_APPLICATION_NAMESPACE, self.access_token)
        else:
            return '%s %s:%s' % (self.conf.ICEBERG_AUTH_HEADER, self.username, self.access_token)

    def get_anonymous_session_id(self):
        """
        Used for anonymous convertion to user
        """
        if self.username != "Anonymous":
            raise IcebergError('User is not anonymous')
        return self.access_token


    def _safe_log(self, logger_function, message, *args):
        if getattr(self.conf, 'UNSECURED_LOGS', False):
            return logger_function(message, *args)

        KEYS_TO_HIDE = ["message_auth", "Authorization", "access_token", "password"]
        safe_args = []
        for arg in args:
            if type(arg) == dict:
                safe_arg = {}
                for key in arg:
                    if key in KEYS_TO_HIDE:
                        safe_arg[key] = 'SECURED'
                    else:
                        safe_arg[key] = arg[key]
                safe_args.append(safe_arg)
            elif isinstance(arg, basestring):
                should_be_secured = False
                for key_to_hide in KEYS_TO_HIDE:
                    if key_to_hide in arg:
                        should_be_secured = True
                        break
                if should_be_secured:
                    safe_args.append('SECURED')
                else:
                    safe_args.append(arg)
            else:
                safe_args.append(arg)

        logger_function(message, *safe_args)


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

        self._safe_log(logger.debug, 'REQUEST %s - %s - %s - GET PARAMS: %s - POST PARAMS: %s', method, url, headers, args, post_args)
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
            self._safe_log(logger.debug, 'RESPONSE %s - %s -  %s', method, url, e.read())
            response = json.loads(e.read())
            raise IcebergAPIError(response)

        try:
            try:
                elapsed = response.elapsed.total_seconds()
            except:
                elapsed = (response.elapsed.days * 1440 + response.elapsed.seconds // 60)*60
            self._safe_log(logger.debug,'RESPONSE - Status: %s - Response Time (s): %s - %s', response.status_code, elapsed, response.text)
        except Exception:
            logger.exception('ERROR in response printing')

        if response.status_code == 401:
            raise IcebergClientUnauthorizedError()
            
        elif 400 <= response.status_code < 500:
            if response.status_code == 404:
                raise IcebergObjectNotFound(response, url = url)
            else:
                raise IcebergClientError(response, url = url)

        elif 500 <= response.status_code <= 600:
            raise IcebergServerError(response)
        
        if response.content:
            return response.json()
        else:
            return "No Content"

