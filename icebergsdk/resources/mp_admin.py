# -*- coding: utf-8 -*-

from icebergsdk.resources.base import IcebergObject


class Transaction(IcebergObject):
    endpoint = 'transaction'


class MarketPlaceTransaction(IcebergObject):
    endpoint = 'mp_transaction'

