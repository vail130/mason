from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Table


class TheTableClassToStringMethod(unittest.TestCase):
    def test_works_by_itself(self):
        table = Table('table')

        self.assertEqual(unicode(table), u'table')
