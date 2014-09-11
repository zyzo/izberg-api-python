# -*- coding: utf-8 -*-

from helper import IcebergUnitTestCase

class ClientAddress(IcebergUnitTestCase):
    def test_create(self):
        self.login()

        offer = self.get_random_offer()

        reviews, meta = self.api_handler.Review.search({
            "offer": offer,
            "user": self.api_handler.me()
        })

        if len(reviews)==0:
            review = self.api_handler.Review()
            review.user = self.api_handler.me()
            review.product_offer = offer

            review.save()

    def test_read(self):
        self.login()

        reviews = self.api_handler.me().reviews()

        self.assertNotEqual(len(reviews), 0)




