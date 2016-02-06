from norm.base import Base
from norm.query.base import Query


class Column(Base):
    def __init__(self, name, table=None, subquery=None, **kwargs):
        self._name = name
        self._table = table
        self._subquery = subquery

        if self._table is None and self._subquery is None:
            raise ValueError('Column instance must have associated Table or SubQuery')

        self._between_start = None
        self._between_end = None
        self._in = None
        self._as = None
        self._on = None
        self._is_null = False
        self._is_not_null = False
        self._asc = False
        self._desc = False

        self.comparison_args = {
            'equal': {'symbol': u'=', 'value': None},
            'not_equal': {'symbol': u'<>', 'value': None},
            'greater': {'symbol': u'>', 'value': None},
            'greater_equal': {'symbol': u'>=', 'value': None},
            'less': {'symbol': u'<', 'value': None},
            'less_equal': {'symbol': u'<=', 'value': None},
        }
        for key in self.comparison_args.viewkeys() & kwargs.viewkeys():
            self.comparison_args[key]['value'] = kwargs[key]

        self.math_args = {
            'add': {'symbol': u'+', 'value': None},
            'sub': {'symbol': u'-', 'value': None},
            'mul': {'symbol': u'*', 'value': None},
            'div': {'symbol': u'/', 'value': None},
        }
        for key in self.math_args.viewkeys() & kwargs.viewkeys():
            self.math_args[key]['value'] = kwargs[key]

    def __eq__(self, other):
        return self.__class__(self._name, self._table, self._subquery, equal=other)

    def __ne__(self, other):
        return self.__class__(self._name, self._table, self._subquery, not_equal=other)

    def __gt__(self, other):
        return self.__class__(self._name, self._table, self._subquery, greater=other)

    def __ge__(self, other):
        return self.__class__(self._name, self._table, self._subquery, greater_equal=other)

    def __lt__(self, other):
        return self.__class__(self._name, self._table, self._subquery, less=other)

    def __le__(self, other):
        return self.__class__(self._name, self._table, self._subquery, less_equal=other)

    def __add__(self, other):
        return self.__class__(self._name, self._table, self._subquery, add=other)

    def __sub__(self, other):
        return self.__class__(self._name, self._table, self._subquery, sub=other)

    def __div__(self, other):
        return self.__class__(self._name, self._table, self._subquery, div=other)

    def __mul__(self, other):
        return self.__class__(self._name, self._table, self._subquery, mul=other)

    def IN(self, arg):
        self._in = arg
        return self

    def BETWEEN(self, start):
        self._between_start = start
        return self

    def AND(self, end):
        if not self._between_start:
            raise NotImplementedError()

        self._between_end = end
        return self

    @property
    def IS_NULL(self):
        if self._is_not_null:
            raise NotImplementedError()

        self._is_null = True
        return self

    @property
    def IS_NOT_NULL(self):
        if self._is_null:
            raise NotImplementedError()

        self._is_not_null = True
        return self

    @property
    def ASC(self):
        if self._desc:
            raise NotImplementedError()

        self._asc = True
        return self

    @property
    def DESC(self):
        if self._asc:
            raise NotImplementedError()

        self._desc = True
        return self

    def AS(self, alias):
        self._as = alias
        return self

    def _to_string(self):
        if self._between_start and not self._between_end:
            raise NotImplementedError()

        if self._table is not None:
            output = u'%s.%s' % (self._table._name, self._name)
        elif self._subquery is not None:
            output = u'%s.%s' % (self._subquery._name, self._name)
        else:
            raise RuntimeError('Column instance must have associated Table or SubQuery')

        is_math_op = False
        is_comparison = False

        for math_arg in self.math_args.itervalues():
            if math_arg['value'] is not None:
                output = u'(%s %s %s)' % (output, math_arg['symbol'], math_arg['value'])
                is_math_op = True
                break

        if not is_math_op:
            for comp_arg in self.comparison_args.itervalues():
                if comp_arg['value'] is not None:
                    output = u'%s %s %s' % (self._as or output, comp_arg['symbol'], comp_arg['value'])
                    is_comparison = True
                    break

        if not is_math_op and not is_comparison:
            if self._in is not None:
                if isinstance(self._in, Query):
                    output = u'%s IN (\n%s\n)' % (output, self._in._to_string(nest_level=1))
                else:
                    output = u'%s IN (%s)' % (output, self._in)
            elif self._between_start and self._between_end:
                output = u'%s BETWEEN %s AND %s' % (output, self._between_start, self._between_end)
            elif self._is_null:
                output = u'%s IS NULL' % output
            elif self._is_not_null:
                output = u'%s IS NOT NULL' % output
            elif self._asc:
                output = u'%s ASC' % output
            elif self._desc:
                output = u'%s DESC' % output
            elif self._as is not None:
                output = u'%s AS %s' % (output, self._as)

        return output
