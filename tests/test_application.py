# -*- coding: utf-8 -*-
from helper import IcebergUnitTestCase
from icebergsdk.api import IcebergAPI
from icebergsdk.exceptions import IcebergClientUnauthorizedError



class TestApplication(IcebergUnitTestCase):

    pass
    def test_01_create(self, namespace=None, name=None, contact_user=None):
        """
        Test Create an Application
        """
        self.direct_login_user_1()
        new_application = self.api_handler.Application()
        new_application.namespace = namespace or "test-app-1"
        new_application.name = name or "Test App 1"
        new_application.contact_user = contact_user or self.api_handler.User.me()
        new_application.save()
        self.api_handler._objects_to_delete.append(new_application)
        return new_application

    def test_02_delete(self, application=None):
        """
        Test Delete an Application
        """
        if application is None:
            application = self.test_01_create()
        application.delete()

    def test_03_sso_read(self):
        """
        Test SSO Read an Application
        - Fetch the application secret key
        - SSO Login on this application
        - Assert authorized read detail by contact_user
        """
        new_application = self.test_01_create()

        PREVIOUS_ICEBERG_APPLICATION_SECRET_KEY = self.api_handler.conf.ICEBERG_APPLICATION_SECRET_KEY
        PREVIOUS_ICEBERG_APPLICATION_NAMESPACE = self.api_handler.conf.ICEBERG_APPLICATION_NAMESPACE
        
        self.api_handler.conf.ICEBERG_APPLICATION_SECRET_KEY = str(new_application.fetch_secret_key())
        self.api_handler.conf.ICEBERG_APPLICATION_NAMESPACE = str(new_application.namespace)

        self.login_user_1()
        application = self.api_handler.Application.find(new_application.id)
        self.assertFalse(application==None)

        self.login_user_2()
        try:
            application = self.api_handler.Application.find(new_application.id)
        except IcebergClientUnauthorizedError:
            ## should raise this exception
            pass
        else:
            raise Exception("Application should not be accessible by user_2")
        
        self.api_handler.conf.ICEBERG_APPLICATION_SECRET_KEY = PREVIOUS_ICEBERG_APPLICATION_SECRET_KEY
        self.api_handler.conf.ICEBERG_APPLICATION_NAMESPACE = PREVIOUS_ICEBERG_APPLICATION_NAMESPACE


    def tearDown(self):
        if hasattr(self.api_handler, "_objects_to_delete"):
            self.direct_login_iceberg_staff()
            for obj in self.api_handler._objects_to_delete:
                try:
                    obj.delete()
                    # print "obj %s deleted" % obj
                except:
                    pass
                    # print "couldnt delete obj %s" % obj

        super(TestApplication, self).tearDown()


