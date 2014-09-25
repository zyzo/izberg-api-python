# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase, get_api_handler
from helpers.login_utils import IcebergLoginUtils


class ClientMerchant(IcebergUnitTestCase):
    @classmethod
    def setUpClass(cls):
        """
        my_context_dict: Create a context dictionary to share some results between tests
        _objects_to_delete: We will delete the created objects after all tests have been done
        """
        cls.my_context_dict = {}
        cls._objects_to_delete = []

        cls.api_handler = get_api_handler()
        IcebergLoginUtils.direct_login(handler = cls.api_handler)

        application = cls.api_handler.Application()
        application.name = "test-merchant-app"
        application.contact_user = cls.api_handler.User.me()
        application.save()

        cls.my_context_dict['application'] = application
        cls._objects_to_delete.append(application)

        # Log user inside the application
        cls.api_handler.access_token = application.auth_me()


    def setUp(self):
        """
        Avoid duplicate api_handler
        """
        pass

    # Account Related tests
    def test_01_create_merchant(self):
        """
        Create contact information for the store
        """
        merchant = self.create_merchant(application = self.my_context_dict['application'])

        self.my_context_dict['merchant'] = merchant
        self._objects_to_delete.append(merchant)


    def test_02_contact_info(self):
        """
        Create contact information for the store
        """
        merchant_address = self.api_handler.MerchantAddress()

        merchant_address.merchant = self.my_context_dict['merchant']
        merchant_address.contact_email = "random@random.com"
        merchant_address.address = "325 random street"    
        merchant_address.city = "Paris"
        merchant_address.zipcode = "75012"
        merchant_address.phone = "0123281398"
        merchant_address.country = self.api_handler.Country.search({'code': 'FR'})[0][0]
        merchant_address.save()

        self._objects_to_delete.append(merchant_address)
    
    

    def test_03_create_bank_account(self):
        """
        """
        bank_account = self.api_handler.StoreBankAccount()

        bank_account.merchant = self.my_context_dict['merchant']
        bank_account.account_BIC = "99898"
        bank_account.account_IBAN = "989898"
        bank_account.account_owner_name = "Florian Poullin"
        bank_account.save()


    # @classmethod
    # def tearDownClass(cls):
    #     pass



