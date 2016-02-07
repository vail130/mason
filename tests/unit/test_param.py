from __future__ import absolute_import, unicode_literals

import unittest

from norm import Param, ANY, COALESCE


class TheParamClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = Param('param')

        self.assertEqual(unicode(param), '%(param)s')


class TheAnyClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = ANY('param')

        self.assertEqual(unicode(param), 'ANY(param)')


class TheCoalesceClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = COALESCE('param', 0)

        self.assertEqual(unicode(param), 'COALESCE(param, 0)')