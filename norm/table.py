from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base
from norm.param import Param
from norm.query.base import Query


class Table(Base):
    def __init__(self, name, column=None, subquery=None):
        self.name = name
        self.column = column
        self.subquery = subquery

        self._between_start = None
        self._between_end = None
        self._in = None
        self._as = None
        self._on = None
        self._not_equal = None
        self._equal = None
        self._greater = None
        self._greater_equal = None
        self._less = None
        self._less_equal = None
        self._is_null = False
        self._is_not_null = False
        self._asc = False
        self._desc = False

    def __getattr__(self, item):
        return Table(self.name, column=item)

    def __eq__(self, other):
        self._equal = other
        return self

    def __ne__(self, other):
        self._not_equal = other
        return self

    def __gt__(self, other):
        self._greater = other
        return self

    def __ge__(self, other):
        self._greater_equal = other
        return self

    def __lt__(self, other):
        self._less = other
        return self

    def __le__(self, other):
        self._less_equal = other
        return self

    def BETWEEN(self, start):
        if not isinstance(start, Param):
            raise NotImplementedError()

        self._between_start = start
        return self

    def IN(self, arg):
        self._in = arg
        return self

    def AND(self, end):
        if not isinstance(end, Param):
            raise NotImplementedError()

        if not self._between_start:
            raise NotImplementedError()

        self._between_end = end
        return self

    def AS(self, alias):
        self._as = alias
        return self

    def ON(self, *args):
        self._on = args
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

    def to_string(self):
        if self._between_start and not self._between_end:
            raise NotImplementedError()

        output = u'%s' % self.name

        if self.column:
            output = u'%s.%s' % (output, self.column)
        elif self.subquery is not None:
            output = u'(\n%s\n) AS %s' % (self.subquery.to_string(nest_level=1), output)

        # Mutually exclusive cases
        if self._as is not None:
            output = u'%s AS %s' % (output, self._as)
        elif self._on is not None:
            output = u'%s ON' % output
            for on in self._on:
                output = u'%s %s' % (output, on)
        elif self._in is not None:
            if isinstance(self._in, Query):
                output = u'%s IN (\n%s\n)' % (output, self._in.to_string(nest_level=1))
            else:
                output = u'%s IN (%s)' % (output, self._in)
        elif self._between_start and self._between_end:
            output = u'%s BETWEEN %s AND %s' % (output, self._between_start, self._between_end)
        elif isinstance(self._equal, (Param, Table)):
            output = u'%s = %s' % (output, self._equal)
        elif isinstance(self._not_equal, (Param, Table)):
            output = u'%s <> %s' % (output, self._not_equal)
        elif isinstance(self._greater, (Param, Table)):
            output = u'%s > %s' % (output, self._equal)
        elif isinstance(self._greater_equal, (Param, Table)):
            output = u'%s >= %s' % (output, self._equal)
        elif isinstance(self._less, (Param, Table)):
            output = u'%s < %s' % (output, self._equal)
        elif isinstance(self._less_equal, (Param, Table)):
            output = u'%s <= %s' % (output, self._equal)
        elif self._is_null:
            output = u'%s IS NULL' % output
        elif self._is_not_null:
            output = u'%s IS NOT NULL' % output
        elif self._asc:
            output = u'%s ASC' % output
        elif self._desc:
            output = u'%s DESC' % output

        return output
