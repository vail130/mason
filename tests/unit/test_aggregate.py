from __future__ import absolute_import, unicode_literals

import unittest

from mason import SUM, COALESCE, Table, Param, COUNT


class TheAggregateClass(unittest.TestCase):
    def test_works_with_coalesce_and_division_with_alias(self):
        table = Table('table')
        category_percent = (SUM(COALESCE(table.column, 0)) / 100.0).AS('category_percent')

        self.assertEqual(str(category_percent),
                         '(SUM(COALESCE(table.column, 0)) / 100.0) AS category_percent')


class TheAggregateClassToStringMethod(unittest.TestCase):
    def test_works_by_itself(self):
        table = Table('table')
        category_percent = SUM(table.column)

        self.assertEqual(str(category_percent),
                         'SUM(table.column)')

    def test_works_with_count_star(self):
        table = Table('table')
        agg = COUNT(table)

        self.assertEqual(str(agg), 'COUNT(*)')

    def test_works_with_alias(self):
        table = Table('table')
        category_percent = SUM(table.column).AS('category_percent')

        self.assertEqual(str(category_percent),
                         'SUM(table.column) AS category_percent')

    def test_works_with_math_operations(self):
        table = Table('table')
        value = Param('value')

        self.assertEqual(str(SUM(table.column) + 100.0), '(SUM(table.column) + 100.0)')
        self.assertEqual(str(SUM(table.column) - 100.0), '(SUM(table.column) - 100.0)')
        self.assertEqual(str(SUM(table.column) * 100.0), '(SUM(table.column) * 100.0)')
        self.assertEqual(str(SUM(table.column) / 100.0), '(SUM(table.column) / 100.0)')

        self.assertEqual(str(SUM(table.column) + 100), '(SUM(table.column) + 100)')
        self.assertEqual(str(SUM(table.column) + value), '(SUM(table.column) + %(value)s)')

    def test_works_with_comparisons(self):
        table = Table('table')
        value = Param('value')

        self.assertEqual(str(SUM(table.column) == value), 'SUM(table.column) = %(value)s')
        self.assertEqual(str(SUM(table.column) != value), 'SUM(table.column) <> %(value)s')
        self.assertEqual(str(SUM(table.column) > value), 'SUM(table.column) > %(value)s')
        self.assertEqual(str(SUM(table.column) >= value), 'SUM(table.column) >= %(value)s')
        self.assertEqual(str(SUM(table.column) < value), 'SUM(table.column) < %(value)s')
        self.assertEqual(str(SUM(table.column) <= value), 'SUM(table.column) <= %(value)s')

        self.assertEqual(str(SUM(table.column) == 100), 'SUM(table.column) = 100')
        self.assertEqual(str(SUM(table.column) == 100.0), 'SUM(table.column) = 100.0')
