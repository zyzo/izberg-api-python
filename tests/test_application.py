# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase
from icebergsdk.api import IcebergAPI
from icebergsdk.exceptions import IcebergClientUnauthorizedError


class TestApplication(IcebergUnitTestCase):
    def test_01_create(self, namespace=None, name=None, contact_user=None):
        """
        Test Create an Application
        """
        self.direct_login_user_1()

        data = {}
        if namespace:
            data['namespace'] = namespace

        if name:
            data['name'] = name

        if contact_user:
            data['contact_user'] = contact_user

        new_application = self.create_application(**data)

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
        previous_conf = self.api_handler.conf
        new_conf = previous_conf() ## here we instanciate the previous conf so that we can modify some values without changing the class values
        new_conf.ICEBERG_APPLICATION_SECRET_KEY = str(new_application.fetch_secret_key())
        new_conf.ICEBERG_APPLICATION_NAMESPACE = str(new_application.namespace)

        self.api_handler = IcebergAPI(conf = new_conf)
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

        self.api_handler.conf = previous_conf


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


