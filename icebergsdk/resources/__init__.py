# -*- coding: utf-8 -*-

from icebergsdk.resources.application import Application  # NoQA
from icebergsdk.resources.order import Order  # NoQA
from icebergsdk.resources.cart import Cart  # NoQA
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation  # NoQA
from icebergsdk.resources.store import Store  # NoQA
from icebergsdk.resources.user import User, Profile  # NoQA
from icebergsdk.resources.address import Address, Country  # NoQA
from icebergsdk.resources.payment import Payment  # NoQA

def get_class_from_resource_uri(resource_uri):
    types = {
        "application": Application,
        "product_offer": ProductOffer,
        "product": Product,
        "user": User,
        "address": Address,
        "profile": Profile,
        "payment": Payment
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if resource in resource_uri:
            return klass

    raise NotImplementedError()

