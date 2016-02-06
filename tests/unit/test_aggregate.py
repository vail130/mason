from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import SUM, COALESCE, Table, Param, COUNT


class TheAggregateClass(unittest.TestCase):
    def test_works_with_coalesce_and_division_with_alias(self):
        table = Table('table')
        category_percent = (SUM(COALESCE(table.column, 0)) / 100.0).AS('category_percent')

        self.assertEqual(unicode(category_percent),
                         u'(SUM(COALESCE(table.column, 0)) / 100.0) AS category_percent')


class TheAggregateClassToStringMethod(unittest.TestCase):
    def test_works_by_itself(self):
        table = Table('table')
        category_percent = SUM(table.column)

        self.assertEqual(unicode(category_percent),
                         u'SUM(table.column)')

    def test_works_with_count_star(self):
        table = Table('table')
        agg = COUNT(table)

        self.assertEqual(unicode(agg), u'COUNT(*)')

    def test_works_with_alias(self):
        table = Table('table')
        category_percent = SUM(table.column).AS('category_percent')

        self.assertEqual(unicode(category_percent),
                         u'SUM(table.column) AS category_percent')

    def test_works_with_math_operations(self):
        table = Table('table')
        value = Param('value')

        self.assertEqual(unicode(SUM(table.column) + 100.0), u'(SUM(table.column) + 100.0)')
        self.assertEqual(unicode(SUM(table.column) - 100.0), u'(SUM(table.column) - 100.0)')
        self.assertEqual(unicode(SUM(table.column) * 100.0), u'(SUM(table.column) * 100.0)')
        self.assertEqual(unicode(SUM(table.column) / 100.0), u'(SUM(table.column) / 100.0)')

        self.assertEqual(unicode(SUM(table.column) + 100), u'(SUM(table.column) + 100)')
        self.assertEqual(unicode(SUM(table.column) + value), u'(SUM(table.column) + %(value)s)')

    def test_works_with_comparisons(self):
        table = Table('table')
        value = Param('value')

        self.assertEqual(unicode(SUM(table.column) == value), u'SUM(table.column) = %(value)s')
        self.assertEqual(unicode(SUM(table.column) != value), u'SUM(table.column) <> %(value)s')
        self.assertEqual(unicode(SUM(table.column) > value), u'SUM(table.column) > %(value)s')
        self.assertEqual(unicode(SUM(table.column) >= value), u'SUM(table.column) >= %(value)s')
        self.assertEqual(unicode(SUM(table.column) < value), u'SUM(table.column) < %(value)s')
        self.assertEqual(unicode(SUM(table.column) <= value), u'SUM(table.column) <= %(value)s')

        self.assertEqual(unicode(SUM(table.column) == 100), u'SUM(table.column) = 100')
        self.assertEqual(unicode(SUM(table.column) == 100.0), u'SUM(table.column) = 100.0')
