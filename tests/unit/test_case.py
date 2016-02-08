from __future__ import absolute_import, unicode_literals

import unittest

from mason import Table, Param, CASE


class TheCaseClassToStringMethod(unittest.TestCase):
    def test_works(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(str(CASE.WHEN(table.column == param).THEN(table.column2).ELSE(0).END),
                         'CASE WHEN table.column = %(param)s THEN table.column2 ELSE 0 END')
