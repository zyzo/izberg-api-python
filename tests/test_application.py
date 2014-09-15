# -*- coding: utf-8 -*-
from copy import copy
from helper import IcebergUnitTestCase
from icebergsdk.api import IcebergAPI
from icebergsdk.exceptions import IcebergClientUnauthorizedError

class TestApplication(IcebergUnitTestCase):


    def test_create(self, namespace=None, name=None, contact_user=None):
        """
        - Create an application
        """
        self.direct_login_user_1()
        new_application = self.api_handler.Application()
        new_application.namespace = namespace or "test-app-1"
        new_application.name = name or "Test App 1"
        new_application.contact_user = contact_user or self.api_handler.User.me()
        new_application.save()
        return new_application

    def test_sso_read(self):
        """
        - Fetch the application secret key
        - SSO Login on this application
        - Assert authorized read detail by contact_user
        """
        new_application = self.test_create()
        
        api_handler = self.api_handler

        new_conf = copy(api_handler.conf)
        new_conf.ICEBERG_APPLICATION_SECRET_KEY = str(new_application.fetch_secret_key())
        new_conf.ICEBERG_APPLICATION_NAMESPACE = str(new_application.namespace)

        self.api_handler = IcebergAPI(conf = new_conf)
        self.login_user_1()
        application = self.api_handler.Application.find(new_application.id)
        self.assertIsNotNone(application)

        self.login_user_2()
        try:
            application = self.api_handler.Application.find(new_application.id)
        except IcebergClientUnauthorizedError:
            ## should raise this exception
            pass
        else:
            raise Exception("Application should not be accessible by user_2")


        self.api_handler = api_handler ## setting back previous api_handler




    # def test_read(self):
    #     self.login_no_sso()
    #     application = self.api_handler.me().application()
    #     self.assertNotEqual(len(application), 0)




