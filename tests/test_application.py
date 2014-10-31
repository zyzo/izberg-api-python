# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from icebergsdk.api import IcebergAPI
from icebergsdk.exceptions import IcebergClientUnauthorizedError


class TestApplication(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_context_dict = {}
        cls._objects_to_delete = []

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

        self._objects_to_delete.append(new_application)
        self.my_context_dict["new_application"] = new_application

        app_found = False
        for app in self.api_handler.User.me().applications():
            if app.id == new_application.id:
                app_found = True
                break
        self.assertTrue(app_found)

        # merchants
        new_application.merchants()

        return new_application

    def test_02_sso_read(self):
        """
        Test SSO Read an Application
        - Fetch the application secret key
        - SSO Login on this application
        - Assert authorized read detail by contact_user
        """
        self.direct_login_user_1()
        new_application = self.my_context_dict["new_application"]
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


    def test_03_delete(self, application=None):
        """
        Test Delete an Application
        """
        self.direct_login_user_1()
        self.my_context_dict["new_application"].delete()

        if self.my_context_dict["new_application"] in self._objects_to_delete:
            ## no need to delete it in tearDownClass if delete succeeded
            self._objects_to_delete.remove(self.my_context_dict["new_application"])


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "_objects_to_delete"):
            api_handler = get_api_handler()
            api_handler.auth_user(username="staff_iceberg", email="staff@iceberg-marketplace.com", is_staff = True)

            for obj in cls._objects_to_delete:
                try:
                    obj.delete(handler = api_handler)
                    # print "obj %s deleted" % obj
                except:
                    pass
                    # print "couldnt delete obj %s" % obj

