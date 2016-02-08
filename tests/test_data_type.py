from __future__ import absolute_import, unicode_literals

import unittest

from mason import TIMESTAMP, DATE, INTERVAL, NUMERIC, DECIMAL, INTEGER


class TheTimestampClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = TIMESTAMP('param')

        self.assertEqual(str(param), '(param)::TIMESTAMP')


class TheIntervalClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = INTERVAL('param')

        self.assertEqual(str(param), '(param)::INTERVAL')


class TheDateClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = DATE('param')

        self.assertEqual(str(param), '(param)::DATE')


class TheNumericClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = NUMERIC('param')

        self.assertEqual(str(param), '(param)::NUMERIC')

    def test_works_with_args(self):
        param = NUMERIC('param', 10, 2)

        self.assertEqual(str(param), '(param)::NUMERIC(10, 2)')


class TheDecimalClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = DECIMAL('param')

        self.assertEqual(str(param), '(param)::DECIMAL')

    def test_works_with_args(self):
        param = DECIMAL('param', 10, 2)

        self.assertEqual(str(param), '(param)::DECIMAL(10, 2)')


class TheIntegerClassToStringMethod(unittest.TestCase):
    def test_works(self):
        param = INTEGER('param')

        self.assertEqual(str(param), '(param)::INTEGER')
