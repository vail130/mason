from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Table, Param, SELECT, AND, OR


class TheSelectClass(unittest.TestCase):
    def test_returns_select_query_string(self):
        p = Table('purchases')
        user_id = Param('user_id')
        start = Param('start')
        end = Param('end')

        query = str(
            SELECT(p.id, p.product_name, p.product_price)
                .FROM(p)
                .WHERE(p.datetime_purchased.BETWEEN(start).AND(end),
                       AND(p.purchaser_id == user_id, OR(p.purchaser_id.IS_NULL)))
                .ORDER_BY(p.datetime_purchased.ASC)
        )

        expected_query = '\n'.join([
            "SELECT purchases.id, purchases.product_name, purchases.product_price",
            "FROM purchases",
            "WHERE purchases.datetime_purchased BETWEEN %(start)s AND %(end)s "
            "AND (purchases.purchaser_id = %(user_id)s OR purchases.purchaser_id IS NULL)",
            "ORDER BY purchases.datetime_purchased ASC",
        ])

        self.assertEqual(query, expected_query)
