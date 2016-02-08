from __future__ import absolute_import, unicode_literals

import unittest

from mason import Table, Param, AND, OR


class TheConditionClassToStringMethod(unittest.TestCase):
    def test_and_works_with_one_argument(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(AND(table.column == param)), 'table.column = %(param)s')

    def test_and_works_with_two_arguments(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(AND(table.column == param, table.column1 < param)),
                         'table.column = %(param)s AND table.column1 < %(param)s')

    def test_or_works_with_one_argument(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(OR(table.column == param)), 'table.column = %(param)s')

    def test_or_works_with_two_arguments(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(OR(table.column == param, table.column1 < param)),
                         'table.column = %(param)s OR table.column1 < %(param)s')

    def test_and_and_or_work_together(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(AND(table.column == param,
                                     OR(table.column1 < param,
                                        table.column2 > param))),
                         'table.column = %(param)s AND (table.column1 < %(param)s OR table.column2 > %(param)s)')
