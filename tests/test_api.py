from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Table, Param, SELECT, AND, OR, COUNT, SUM


class TheSelectClass(unittest.TestCase):
    def test_returns_select_query_string(self):
        purchases = Table('purchases')
        users = Table('users')
        user_id = Param('user_id')
        start = Param('start')
        end = Param('end')

        query = str(
            SELECT(purchases.id, purchases.product_name, purchases.product_price)
                .FROM(purchases)
                .INNER_JOIN(users.ON(purchases.purchaser_id == users.user_id))
                .WHERE(purchases.datetime_purchased.BETWEEN(start).AND(end),
                       AND(purchases.purchaser_id == user_id, OR(purchases.purchaser_id.IS_NULL)))
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

    def test_returns_select_query_grouping_string(self):
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
