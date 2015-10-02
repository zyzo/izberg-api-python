# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject
from icebergsdk.exceptions import IcebergNoHandlerError


class User(IcebergObject):
    endpoint = 'user'

    # @classmethod
    # def me(cls):
    #     if not cls._handler:
    #         raise IcebergNoHandlerError()

    #     data = cls._handler.request("%s/me/" % (cls.endpoint))
    #     return cls.findOrCreate(data)

    @classmethod
    def me(cls, handler):
        if not handler:
            raise IcebergNoHandlerError()

        data = handler.request("%s/me/" % (cls.endpoint))
        return cls.findOrCreate(handler, data)

    def addresses(self, args=None):
        """
        Get the user's addresses

        Parameters:
            - args: Optional dict of args to restrict search
        Returns:
            - List of results
        """
        if not args:
            args = {}
        args['user'] = self.id
        return self.get_list('address', args=args)

    def applications(self, args=None):
        """
        Get the user's applications

        Parameters:
            - args: Optional dict of args to restrict search
        Returns:
            - List of results
        """
        if not args:
            args = {}
        args['contact_user'] = self.id
        return self.get_list('application', args=args)

    def reviews(self, args=None):
        """
        Get the user's reviews

        Parameters:
            - args: Optional dict of args to restrict search
        Returns:
            - List of results
        """
        if not args:
            args = {}
        args['user'] = self.id
        return self.get_list('review', args=args)

    def orders(self, args=None):
        """
        Get the user's orders

        Parameters:
            - args: Optional dict of args to restrict search
        Returns:
            - List of results
        """
        if not args:
            args = {}
        args['user'] = self.id
        return self.get_list('order', args=args)

    def profile(self):
        data = self.request('%sprofile/' % self.resource_uri)
        return Profile.findOrCreate(self._handler, data)

    # Messages
    def inbox(self):
        return self.get_list("%sinbox/" % self.resource_uri)

    def outbox(self):
        return self.get_list("%soutbox/" % self.resource_uri)


class Profile(UpdateableIcebergObject):
    endpoint = 'profile'


class UserShoppingPreference(UpdateableIcebergObject):
    endpoint = 'user_shopping_prefs'
