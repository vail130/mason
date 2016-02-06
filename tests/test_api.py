from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Table, Param, SELECT, AND, OR, COUNT, SUM, ANY


class TheSelectClass(unittest.TestCase):
    def test_returns_string_for_select_query(self):
        purchases = Table('purchases')
        users = Table('users')
        user_id = Param('user_id')
        start = Param('start')
        end = Param('end')

        query = str(
            SELECT(purchases.id, purchases.product_name, purchases.product_price)
                .FROM(purchases)
                .INNER_JOIN(users.ON(purchases.purchaser_id == users.user_id))
                .WHERE(AND(purchases.datetime_purchased.BETWEEN(start).AND(end),
                           OR(purchases.purchaser_id == user_id,
                              purchases.purchaser_id.IS_NULL)))
                .ORDER_BY(purchases.datetime_purchased.ASC)
                .LIMIT(10)
                .OFFSET(10)
        )

        expected_query = '\n'.join([
            "SELECT purchases.id, purchases.product_name, purchases.product_price",
            "FROM purchases",
            "INNER JOIN users ON purchases.purchaser_id = users.user_id",
            "WHERE purchases.datetime_purchased BETWEEN %(start)s AND %(end)s "
            "AND (purchases.purchaser_id = %(user_id)s OR purchases.purchaser_id IS NULL)",
            "ORDER BY purchases.datetime_purchased ASC",
            "LIMIT 10",
            "OFFSET 10",
        ])

        self.assertEqual(query, expected_query)

    def test_returns_string_for_select_query_grouping(self):
        purchases = Table('purchases')
        start = Param('start')
        end = Param('end')
        min_category_sum = Param('min_category_sum')

        num_purchases = COUNT(purchases).AS('num_purchases')
        category_sum = SUM(purchases.product_price).AS('category_sum')
        query = str(
            SELECT(purchases.category, category_sum, num_purchases)
                .FROM(purchases)
                .WHERE(purchases.datetime_purchased.BETWEEN(start).AND(end))
                .GROUP_BY(purchases.category)
                .HAVING(category_sum > min_category_sum)
        )

        expected_query = '\n'.join([
            "SELECT purchases.category, SUM(purchases.product_price) AS category_sum, COUNT(*) AS num_purchases",
            "FROM purchases",
            "WHERE purchases.datetime_purchased BETWEEN %(start)s AND %(end)s",
            "GROUP BY purchases.category",
            "HAVING category_sum > %(min_category_sum)s",
        ])

        self.assertEqual(query, expected_query)

    def test_returns_string_for_select_query_with_subqueries(self):
        purchases = Table('purchases')
        num_purchases = COUNT(purchases).AS('num_purchases')
        grouped_purchases = (
            SELECT(purchases.category.AS('category'), num_purchases)
                .FROM(purchases)
                .GROUP_BY(purchases.category)
                .AS('grouped_purchases')
        )

        products = Table('products')
        num_products = COUNT(products).AS('num_products')
        grouped_products = (
            SELECT(products.category.AS('category'), num_products)
                .FROM(products)
                .GROUP_BY(products.category)
                .AS('grouped_products')
        )

        categories = Param('categories')
        query = str(
            SELECT(grouped_purchases.category, grouped_purchases.num_purchases, grouped_products.num_products)
                .FROM(grouped_purchases)
                .INNER_JOIN(grouped_products.ON(grouped_purchases.category == grouped_products.category))
                .WHERE(grouped_purchases.category == ANY(categories))
        )

        expected_query = '\n'.join([
            "SELECT grouped_purchases.category, grouped_purchases.num_purchases, grouped_products.num_products",
            "FROM (",
            "\tSELECT purchases.category AS category, COUNT(*) AS num_purchases",
            "\tFROM purchases",
            "\tGROUP BY purchases.category",
            ") AS grouped_purchases",
            "INNER JOIN (",
            "\tSELECT products.category AS category, COUNT(*) AS num_products",
            "\tFROM products",
            "\tGROUP BY products.category",
            ") AS grouped_products ON grouped_purchases.category = grouped_products.category",
            "WHERE grouped_purchases.category = ANY(%(categories)s)",
        ])

        self.assertEqual(query, expected_query)
