# -*- coding: utf-8 -*-

class IcebergLoginUtils(object):
    """
    Some utils to login as regular user, application staff or staff
    """
    # Anonymous
    @classmethod
    def login_anonymous(cls, handler):
        handler.sso_user()

    # User 1
    @classmethod
    def login(cls, handler):
        handler.sso_user(email = "lol@lol.fr", first_name = "Yves", last_name = "Durand")

    @classmethod
    def direct_login(cls, handler):
        handler.auth_user(username="yvesdurand5269004", email="lol@lol.fr")


    # User 2
    @classmethod
    def login_user_2(cls, handler):
        handler.sso_user(email = "user2@izberg-marketplace.com", first_name = "Sara", last_name = "Crôche")

    @classmethod
    def direct_login_user_2(cls, handler):
        handler.auth_user(username="saracroche", email="user2@izberg-marketplace.com")

    # User        
    @classmethod
    def login_user_1(cls, handler):
        handler.sso_user(email = "user1@izberg-marketplace.com", first_name = "Jeff", last_name = "Strongman")

    @classmethod
    def direct_login_user_1(cls, handler):
        handler.auth_user(username="jeffstrongman", email="user1@izberg-marketplace.com")


    # Staff
    @classmethod
    def direct_login_iceberg_staff(cls, handler):
        handler.auth_user(username="staff_iceberg", email="staff@izberg-marketplace.com", is_staff = True)



