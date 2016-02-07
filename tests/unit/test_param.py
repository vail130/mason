from __future__ import absolute_import
from __future__ import print_function

import unittest

from norm import Param, ANY, COALESCE


class TheParamClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = Param('param')

        self.assertEqual(unicode(param), u'%(param)s')


class TheAnyClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = ANY('param')

        self.assertEqual(unicode(param), u'ANY(param)')


class TheCoalesceClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = COALESCE('param', 0)

        self.assertEqual(unicode(param), u'COALESCE(param, 0)')
