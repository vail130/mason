from __future__ import absolute_import, unicode_literals

import unittest

from norm import Table, Param, SELECT
from norm.column import Column


class TheColumnClassToStringMethod(unittest.TestCase):
    def setUp(self):
        self.table = Table('table')
        self.param = Param('param')

    def test_works_with_null_comparisons(self):
        self.assertEqual(Column('column', table=self.table).IS_NULL._to_string(), 'table.column IS NULL')
        self.assertEqual(Column('column', table=self.table).IS_NOT_NULL._to_string(), 'table.column IS NOT NULL')

    def test_works_with_order_direction(self):
        self.assertEqual(Column('column', table=self.table).ASC._to_string(), 'table.column ASC')
        self.assertEqual(Column('column', table=self.table).DESC._to_string(), 'table.column DESC')

    def test_works_with_between_comparison(self):
        self.assertEqual(unicode(Column('column', table=self.table).BETWEEN(self.param).AND(self.param)),
                         'table.column BETWEEN %(param)s AND %(param)s')
        self.assertEqual(unicode(Column('column', table=self.table).BETWEEN(Column('column', table=self.table)).AND(
            Column('column', table=self.table))),
            'table.column BETWEEN table.column AND table.column')

    def test_works_with_math_operations(self):
        self.assertEqual(unicode(Column('column', table=self.table) + 100.0), '(table.column + 100.0)')
        self.assertEqual(unicode(Column('column', table=self.table) - 100.0), '(table.column - 100.0)')
        self.assertEqual(unicode(Column('column', table=self.table) * 100.0), '(table.column * 100.0)')
        self.assertEqual(unicode(Column('column', table=self.table) / 100.0), '(table.column / 100.0)')

        self.assertEqual(unicode(Column('column', table=self.table) + 100), '(table.column + 100)')
        self.assertEqual(unicode(Column('column', table=self.table) + self.param), '(table.column + %(param)s)')

    def test_works_with_comparisons(self):
        self.assertEqual(unicode(Column('column', table=self.table) == 100.0), 'table.column = 100.0')
        self.assertEqual(unicode(Column('column', table=self.table) != 100.0), 'table.column <> 100.0')
        self.assertEqual(unicode(Column('column', table=self.table) > 100.0), 'table.column > 100.0')
        self.assertEqual(unicode(Column('column', table=self.table) >= 100.0), 'table.column >= 100.0')
        self.assertEqual(unicode(Column('column', table=self.table) < 100.0), 'table.column < 100.0')
        self.assertEqual(unicode(Column('column', table=self.table) <= 100.0), 'table.column <= 100.0')

        self.assertEqual(unicode(Column('column', table=self.table) == 100), 'table.column = 100')
        self.assertEqual(unicode(Column('column', table=self.table) == self.param), 'table.column = %(param)s')

    def test_works_with_in(self):
        subquery = SELECT(Column('column1', table=self.table)).FROM(self.table)

        self.assertEqual(unicode(Column('column', table=self.table).IN(self.param)), 'table.column IN (%(param)s)')
        self.assertEqual(unicode(Column('column', table=self.table).IN(subquery)),
                         'table.column IN (\n\tSELECT table.column1\n\tFROM table\n)')

    def test_works_with_as(self):
        self.assertEqual(unicode(Column('column', table=self.table).AS('alias')), 'table.column AS alias')
