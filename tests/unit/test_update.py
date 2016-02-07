from __future__ import absolute_import, unicode_literals

import unittest

from norm import Param, Table, UPDATE, AND


class TheUpdateClass(unittest.TestCase):
    def test_returns_string_for_update_query(self):
        purchases = Table('purchases')
        discount_percent = Param('discount_percent')

        query = unicode(
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

        query = unicode(
            UPDATE(purchases)
                .SET(product_price=new_price,
                     sale_price=purchases.product_price * discount_percent)
                .WHERE(purchases.product_price > 200)
        )

        self.assertIn("purchases.product_price = %(new_price)s", query)
        self.assertIn("purchases.sale_price = (purchases.product_price * %(discount_percent)s)", query)

    def test_returns_string_for_update_query_with_from(self):
        purchases = Table('purchases')
        discounts = Table('discounts')

        query = unicode(
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
