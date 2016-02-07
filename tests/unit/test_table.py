from __future__ import absolute_import, unicode_literals

import unittest

from norm import Table


class TheTableClassToStringMethod(unittest.TestCase):
    def test_works_by_itself(self):
        table = Table('table')

        self.assertEqual(str(table), 'table')
