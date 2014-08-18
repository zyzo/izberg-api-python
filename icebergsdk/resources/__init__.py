# -*- coding: utf-8 -*-

import logging

from icebergsdk.resources.application import Application  # NoQA
from icebergsdk.resources.order import Order, MerchantOrder, OrderItem  # NoQA
from icebergsdk.resources.cart import Cart, CartItem  # NoQA
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation  # NoQA
from icebergsdk.resources.store import Store  # NoQA
from icebergsdk.resources.user import User, Profile  # NoQA
from icebergsdk.resources.address import Address, Country  # NoQA
from icebergsdk.resources.payment import Payment  # NoQA
from icebergsdk.resources.message import Message  # NoQA

logger = logging.getLogger('icebergsdk')

def get_class_from_resource_uri(resource_uri):
    types = {
        "application": Application,
        "product": Product,
        "product_offer": ProductOffer,
        "product_variation": ProductVariation,
        "user": User,
        "address": Address,
        "country": Country,
        "profile": Profile,
        "payment": Payment,
        "merchant": Store,
        "order": Order,
        "merchant_order": MerchantOrder,
        "message": Message,
        "cart": Cart,
        "cart_item": CartItem,
        "order_item": OrderItem
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if resource in resource_uri:
            return klass

    logger.error('cant find resource for %s' % resource_uri)
    raise NotImplementedError()

