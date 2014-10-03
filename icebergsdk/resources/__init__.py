# -*- coding: utf-8 -*-

import logging

from icebergsdk.resources.application import Application, ApplicationCommissionSettings
from icebergsdk.resources.order import Order, MerchantOrder, OrderItem
from icebergsdk.resources.cart import Cart, CartItem
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation, ProductOfferImage, Category, Brand
from icebergsdk.resources.store import Store, MerchantImage, MerchantAddress, StoreBankAccount, MerchantCommissionSettings
from icebergsdk.resources.user import User, Profile, UserShoppingPreference
from icebergsdk.resources.address import Address, Country
from icebergsdk.resources.payment import Payment
from icebergsdk.resources.message import Message
from icebergsdk.resources.review import Review, MerchantReview
from icebergsdk.resources.webhooks import Webhook, WebhookTrigger, WebhookTriggerAttempt

logger = logging.getLogger('icebergsdk')

def get_class_from_resource_uri(resource_uri):
    types = {
        "application": Application,
        "application_commission_settings": ApplicationCommissionSettings,
        "product": Product,
        "brand": Brand,
        "productoffer": ProductOffer,
        "offer_image": ProductOfferImage,
        "product_variation": ProductVariation,
        "user": User,
        "address": Address,
        "country": Country,
        "brand": Brand,
        "profile": Profile,
        "user_shopping_prefs": UserShoppingPreference, 
        "payment": Payment,
        "merchant": Store,
        "store_bank_account": StoreBankAccount,
        "commission_settings": MerchantCommissionSettings,
        "merchant_address": MerchantAddress,
        "merchant_image": MerchantImage,
        "order": Order,
        "merchant_order": MerchantOrder,
        "message": Message,
        "cart": Cart,
        "cart_item": CartItem,
        "order_item": OrderItem,
        "review": Review,
        "merchant_review": MerchantReview,
        "category": Category,
        "brand": Brand,
        "webhook": Webhook,
        "webhook_trigger": WebhookTrigger,
        "webhook_trigger_attempt": WebhookTriggerAttempt,
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if "/%s/" % resource in resource_uri:
            return klass

    logger.error('cant find resource for %s' % resource_uri)
    raise NotImplementedError()

