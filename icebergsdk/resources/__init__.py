# -*- coding: utf-8 -*-

import logging

from icebergsdk.resources.application import Application, ApplicationCommissionSettings, ApplicationMerchantPolicies,\
    ApplicationTransaction, ApplicationPaymentSettings, ApplicationUrls, ApplicationPermission
from icebergsdk.resources.order import Order, MerchantOrder, OrderItem
from icebergsdk.resources.cart import Cart, CartItem
from icebergsdk.resources.product import Product, ProductOffer, ProductVariation, ProductOfferImage, Category, Brand,\
    ProductFamily, ProductFamilySelector, Image
from icebergsdk.resources.store import Store, MerchantImage, MerchantAddress, StoreBankAccount,\
    MerchantCommissionSettings, MerchantFeed, MerchantShippingPolicy,\
    MerchantTransaction, Permission
from icebergsdk.resources.user import User, Profile, UserShoppingPreference
from icebergsdk.resources.address import Address, Country
from icebergsdk.resources.payment import Payment
from icebergsdk.resources.message import Message
from icebergsdk.resources.review import Review, MerchantReview
from icebergsdk.resources.webhooks import Webhook, WebhookTrigger, WebhookTriggerAttempt
from icebergsdk.resources.currency import Currency
from icebergsdk.resources.mp_admin import Transaction, MarketPlaceTransaction
from icebergsdk.resources.return_refund import Return, Refund
from icebergsdk.resources.channels import ProductChannel, ChannelPropagationPolicy, ProductChannelLogEvent
from icebergsdk.resources.service import ServiceOffer, ServiceOfferVariation, ServiceOption
from icebergsdk.resources.timeslots import (
    AvailabilityCalendar, AvailabilityTimeSlot, Reservation)
from icebergsdk.resources.options import Option, OptionAnswer


logger = logging.getLogger('icebergsdk')


def get_class_from_resource_uri(resource_uri):
    types = {
        "application": Application,
        "application_commission_settings": ApplicationCommissionSettings,
        "app_payment_settings": ApplicationPaymentSettings,
        "app_permission": ApplicationPermission,
        "application_merchant_policies": ApplicationMerchantPolicies,
        "application_urls": ApplicationUrls,
        "app_transaction": ApplicationTransaction,
        "mp_transaction": MarketPlaceTransaction,
        "product": Product,
        "brand": Brand,
        "currency": Currency,
        "productoffer": ProductOffer,
        "offer_image": ProductOfferImage,
        "product_variation": ProductVariation,
        "user": User,
        "address": Address,
        "country": Country,
        "profile": Profile,
        "user_shopping_prefs": UserShoppingPreference,
        "payment": Payment,
        "image": Image,
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
        "webhook": Webhook,
        "webhook_trigger": WebhookTrigger,
        "webhook_trigger_attempt": WebhookTriggerAttempt,
        "merchant_catalog_feed": MerchantFeed,
        "merchant_shipping_policy": MerchantShippingPolicy,
        "store_transaction": MerchantTransaction,
        "transaction": Transaction,
        "return": Return,
        "refund": Refund,
        "permission": Permission,
        "product_channel": ProductChannel,
        "product_channel_propagation_policy": ChannelPropagationPolicy,
        "product_channel_log_event": ProductChannelLogEvent,
        "product_family": ProductFamily,
        "product_family_selector": ProductFamilySelector,
        "service_offer": ServiceOffer,
        "service_option": ServiceOption,
        "service_offer_variation": ServiceOfferVariation,
        "availability_calendar": AvailabilityCalendar,
        "availability_timeslot": AvailabilityTimeSlot,
        "reservation": Reservation,
        "option": Option,
        "option_answer": OptionAnswer
    }

    # Hack for now... Will be changed
    for resource, klass in types.iteritems():
        if "/%s/" % resource in resource_uri:
            return klass

    logger.error('cant find resource for %s' % resource_uri)
    raise NotImplementedError()
