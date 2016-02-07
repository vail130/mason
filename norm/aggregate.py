from __future__ import absolute_import, unicode_literals

from norm.base import Base


class Aggregate(Base):
    TYPE = None

    def __init__(self, field, **kwargs):
        if self.TYPE is None:
            raise NotImplementedError('subclasses of Aggregate must define TYPE class variable')

        self.field = field
        self._as = kwargs.get('_as')

        self.comparison_args = {
            'equal': {'symbol': '=', 'value': None},
            'not_equal': {'symbol': '<>', 'value': None},
            'greater': {'symbol': '>', 'value': None},
            'greater_equal': {'symbol': '>=', 'value': None},
            'less': {'symbol': '<', 'value': None},
            'less_equal': {'symbol': '<=', 'value': None},
        }
        for key in self.comparison_args.viewkeys() & kwargs.viewkeys():
            self.comparison_args[key]['value'] = kwargs[key]

        self.math_args = {
            'add': {'symbol': '+', 'value': None},
            'sub': {'symbol': '-', 'value': None},
            'mul': {'symbol': '*', 'value': None},
            'div': {'symbol': '/', 'value': None},
        }
        for key in self.math_args.viewkeys() & kwargs.viewkeys():
            self.math_args[key]['value'] = kwargs[key]

    def AS(self, alias):
        self._as = alias
        return self

    def __eq__(self, other):
        return self.__class__(self.field, _as=self._as, equal=other)

    def __ne__(self, other):
        return self.__class__(self.field, _as=self._as, not_equal=other)

    def __gt__(self, other):
        return self.__class__(self.field, _as=self._as, greater=other)

    def __ge__(self, other):
        return self.__class__(self.field, _as=self._as, greater_equal=other)

    def __lt__(self, other):
        return self.__class__(self.field, _as=self._as, less=other)

    def __le__(self, other):
        return self.__class__(self.field, _as=self._as, less_equal=other)

    def __add__(self, other):
        return self.__class__(self.field, _as=self._as, add=other)

    def __sub__(self, other):
        return self.__class__(self.field, _as=self._as, sub=other)

    def __div__(self, other):
        return self.__class__(self.field, _as=self._as, div=other)

    def __mul__(self, other):
        return self.__class__(self.field, _as=self._as, mul=other)

    def _to_string(self):
        if self.field.__class__.__name__ == 'Table':
            output = '%s(*)' % self.TYPE
        else:
            output = '%s(%s)' % (self.TYPE, self.field)

        for math_arg in self.math_args.itervalues():
            if math_arg['value'] is not None:
                output = '(%s %s %s)' % (output, math_arg['symbol'], math_arg['value'])
                break

        is_comparison = False
        for comp_arg in self.comparison_args.itervalues():
            if comp_arg['value'] is not None:
                output = '%s %s %s' % (self._as or output, comp_arg['symbol'], comp_arg['value'])
                is_comparison = True
                break

        if not is_comparison and self._as is not None:
            output = '%s AS %s' % (output, self._as)

        return output


class COUNT(Aggregate):
    TYPE = 'COUNT'


class SUM(Aggregate):
    TYPE = 'SUM'


class MAX(Aggregate):
    TYPE = 'MAX'


class MIN(Aggregate):
    TYPE = 'MIN'
