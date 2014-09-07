# -*- coding: utf-8 -*-

import logging

from icebergsdk.resources.application import Application
from icebergsdk.resources.order import Order, MerchantOrder, OrderItem
from icebergsdk.resources.cart import Cart, CartItem
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation
from icebergsdk.resources.store import Store
from icebergsdk.resources.user import User, Profile
from icebergsdk.resources.address import Address, Country
from icebergsdk.resources.payment import Payment
from icebergsdk.resources.message import Message
from icebergsdk.resources.review import Review, MerchantReview

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
        "order_item": OrderItem,
        "review": Review,
        "merchant_review": MerchantReview
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if resource in resource_uri:
            return klass

    logger.error('cant find resource for %s' % resource_uri)
    raise NotImplementedError()

