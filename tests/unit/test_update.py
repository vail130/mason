from __future__ import absolute_import, unicode_literals

import unittest

from norm import Param, Table, UPDATE, AND, SELECT, COUNT


class TheUpdateClass(unittest.TestCase):
    def test_returns_string_for_update_query(self):
        purchases = Table('purchases')
        discount_percent = Param('discount_percent')

        query = str(
            UPDATE(purchases)
                .SET(sale_price=purchases.product_price * discount_percent)
                .WHERE(purchases.product_price > 200)
        )

        expected_query = '\n'.join([
            "UPDATE purchases",
            "SET purchases.sale_price = (purchases.product_price * %(discount_percent)s)",
            "WHERE purchases.product_price > 200",
        ])

        self.assertEqual(query, expected_query)

    def test_returns_string_with_multi_set(self):
        purchases = Table('purchases')
        new_price = Param('new_price')
        discount_percent = Param('discount_percent')

        query = str(
            UPDATE(purchases)
                .SET(product_price=new_price,
                     sale_price=purchases.product_price * discount_percent)
                .WHERE(purchases.product_price > 200)
        )

        self.assertTrue("purchases.product_price = %(new_price)s" in query)
        self.assertTrue("purchases.sale_price = (purchases.product_price * %(discount_percent)s)" in query)

    def test_returns_string_for_update_query_with_from(self):
        purchases = Table('purchases')
        discounts = Table('discounts')

        query = str(
            UPDATE(purchases)
                .SET(sale_price=purchases.product_price * discounts.discount_percent)
                .FROM(discounts)
                .WHERE(AND(purchases.product_price > 200,
                           purchases.product_id == discounts.product_id))
        )

        expected_query = '\n'.join([
            "UPDATE purchases",
            "SET purchases.sale_price = (purchases.product_price * discounts.discount_percent)",
            "FROM discounts",
            "WHERE purchases.product_price > 200 AND purchases.product_id = discounts.product_id",
        ])

        self.assertEqual(query, expected_query)

    def test_returns_string_for_update_query_with_from_subquery(self):
        purchases = Table('purchases')
        discount_percent = Param('discount_percent')

        num_purchases = COUNT(purchases).AS('num_purchases')
        popular_products = (
            SELECT(purchases.product_id, num_purchases)
                .FROM(purchases)
                .GROUP_BY(purchases.product_id)
                .HAVING(num_purchases > 10)
                .AS('popular_products')
        )

        query = str(
            UPDATE(purchases)
                .SET(sale_price=purchases.product_price * discount_percent)
                .FROM(popular_products)
                .WHERE(purchases.product_id == popular_products.product_id)
        )

        expected_query = '\n'.join([
            "UPDATE purchases",
            "SET purchases.sale_price = (purchases.product_price * %(discount_percent)s)",
            "FROM (",
            "\tSELECT purchases.product_id, COUNT(*) AS num_purchases",
            "\tFROM purchases",
            "\tGROUP BY purchases.product_id",
            "\tHAVING num_purchases > 10",
            ") AS popular_products",
            "WHERE purchases.product_id = popular_products.product_id",
        ])

        self.assertEqual(query, expected_query)
