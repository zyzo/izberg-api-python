# -*- coding: utf-8 -*-

import os

class Configuration:
    ICEBERG_API_URL = "https://api.iceberg.technology"
    ICEBERG_API_PORT = 443

    ICEBERG_CORS = "https://api.iceberg.technology:%s/cors/" % (ICEBERG_API_PORT)

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"
    ICEBERG_ENV = "prod"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY', None)


class ConfigurationSandbox:
    ICEBERG_API_URL = "http://api.sandbox.iceberg.technology"
    ICEBERG_API_PORT = 80

    ICEBERG_CORS = "http://api.sandbox.iceberg.technology/cors/"

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"
    ICEBERG_ENV = "sandbox"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_SANDBOX', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_SANDBOX', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_SANDBOX', None)

