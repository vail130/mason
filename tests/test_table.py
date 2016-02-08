from __future__ import absolute_import, unicode_literals

import unittest

from mason import Table


class TheTableClassToStringMethod(unittest.TestCase):
    def test_works_by_itself(self):
        table = Table('table')

        self.assertEqual(str(table), 'table')

    def test_works_with_as(self):
        table = Table('table')

        self.assertEqual(str(table.AS('t')), 'table AS t')

    def test_works_with_on(self):
        table = Table('table')

        self.assertEqual(str(table.ON(table.a == table.b)), 'table ON table.a = table.b')
