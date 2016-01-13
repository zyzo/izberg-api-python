# -*- coding: utf-8 -*-

import os


class ConfigurationBase(object):
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"
    ICEBERG_MODULES_URL = "http://connect.iceberg-marketplace.com/modules/"

    ICEBERG_API_URL = None
    ICEBERG_API_PORT = None
    ICEBERG_CORS = None
    ICEBERG_API_URL_FULL = None
    ICEBERG_ENV = None

    ICEBERG_API_PRIVATE_KEY = None
    ICEBERG_APPLICATION_NAMESPACE = None
    ICEBERG_APPLICATION_SECRET_KEY = None

    IMAGE_SERVER_URL = None


class Configuration(ConfigurationBase):

    """
    Main Configuration. Use for Production
    """
    ICEBERG_API_URL = "https://api.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_CORS = "https://api.iceberg.technology:%s/cors/" % (ICEBERG_API_PORT)
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "prod"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', "https://d2isoz0l8l3l8c.cloudfront.net")


class ConfigurationSandbox(ConfigurationBase):

    """
    Sandbox Configuration. Isolated from Production.
    """
    ICEBERG_API_URL = "https://api.sandbox.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_CORS = "https://api.sandbox.iceberg.technology/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "sandbox"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_SANDBOX', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_SANDBOX', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_SANDBOX', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', "https://d2isoz0l8l3l8c.cloudfront.net")


class ConfigurationSandboxStage(ConfigurationBase):

    """
    Sandbox Configuration. Isolated from Production.
    """
    ICEBERG_API_URL = "https://api.sandbox.stage.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_CORS = "https://api.sandbox.stage.iceberg.technology/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "sandbox_stage"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_SANDBOX_STAGE', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_SANDBOX_STAGE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_SANDBOX_STAGE', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', "https://d2isoz0l8l3l8c.cloudfront.net")


class ConfigurationStage(ConfigurationBase):

    """
    PreProd configuration. Share same database as Prod
    """
    ICEBERG_API_URL = "https://api.stage.iceberg.technology"
    ICEBERG_API_PORT = 443
    ICEBERG_CORS = "https://api.stage.iceberg.technology/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_ENV = "stage"

    # Keys
    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_STAGE', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_STAGE', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_STAGE', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', "https://d2isoz0l8l3l8c.cloudfront.net")

######
# Development Configuration. Use for local development.
######


class ConfigurationDebug(ConfigurationBase):
    ICEBERG_API_URL = "http://api.local.iceberg.technology"
    ICEBERG_API_PORT = 8000
    ICEBERG_ENV = "prod"
    ICEBERG_CORS = "http://api.local.iceberg.technology:8000/cors/"
    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    UNSECURED_LOGS = True

    ICEBERG_MODULES_URL = "http://connect.local.iceberg-marketplace.com:9000/modules/"

    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_DEBUG', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_DEBUG', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_DEBUG', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', None)


class ConfigurationDebugSandbox(ConfigurationDebug):
    ICEBERG_API_URL = "http://api.sandbox.local.iceberg.technology"
    ICEBERG_CORS = "http://api.sandbox.local.iceberg.technology:8000/cors/"
    ICEBERG_ENV = "sandbox"

    ICEBERG_API_PRIVATE_KEY = os.getenv('ICEBERG_API_PRIVATE_KEY_DEBUG_SANDBOX', None)
    ICEBERG_APPLICATION_NAMESPACE = os.getenv('ICEBERG_APPLICATION_NAMESPACE_DEBUG_SANDBOX', None)
    ICEBERG_APPLICATION_SECRET_KEY = os.getenv('ICEBERG_APPLICATION_SECRET_KEY_DEBUG_SANDBOX', None)

    IMAGE_SERVER_URL = os.getenv('ICEBERG_IMAGE_SERVER_URL', None)
