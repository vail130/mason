from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Table, Param, CASE


class TheCaseClassToStringMethod(unittest.TestCase):
    def test_and_works_with_one_argument(self):
        table = Table('table')
        param = Param('param')

        self.assertEqual(unicode(CASE.WHEN(table.column == param).THEN(table.column2).ELSE(0).END),
                         u'CASE WHEN table.column = %(param)s THEN table.column2 ELSE 0 END')
