from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base
from norm.param import Param
from norm.table import Table

__ALL__ = ['COUNT', 'SUM']


class Aggregate(Base):
    TYPE = None

    def __init__(self, field, **kwargs):
        if self.TYPE is None:
            raise NotImplementedError()

        if not field:
            raise NotImplementedError()

        self.field = field
        self._as = kwargs.get('_as')
        self._equal = kwargs.get('_equal')
        self._not_equal = kwargs.get('_not_equal')
        self._greater = kwargs.get('_greater')
        self._greater_equal = kwargs.get('_greater_equal')
        self._less = kwargs.get('_less')
        self._less_equal = kwargs.get('_less_equal')

    def AS(self, alias):
        self._as = alias
        return self

    def __eq__(self, other):
        return self.__class__(self.field, _as=self._as, _equal=other)

    def __ne__(self, other):
        return self.__class__(self.field, _as=self._as, _not_equal=other)

    def __gt__(self, other):
        return self.__class__(self.field, _as=self._as, _greater=other)

    def __ge__(self, other):
        return self.__class__(self.field, _as=self._as, _greater_equal=other)

    def __lt__(self, other):
        return self.__class__(self.field, _as=self._as, _less=other)

    def __le__(self, other):
        return self.__class__(self.field, _as=self._as, _less_equal=other)

    def to_string(self):
        if not isinstance(self.field, Table):
            raise NotImplementedError()

        if not self.field.column:
            output = u'%s(*)' % self.TYPE
        else:
            output = u'%s(%s)' % (self.TYPE, self.field)

        if self._as is not None:
            if isinstance(self._equal, (Param, Table)):
                output = u'%s = %s' % (self._as, self._equal)
            elif isinstance(self._not_equal, (Param, Table)):
                output = u'%s <> %s' % (self._as, self._not_equal)
            elif isinstance(self._greater, (Param, Table)):
                output = u'%s > %s' % (self._as, self._greater)
            elif isinstance(self._greater_equal, (Param, Table)):
                output = u'%s >= %s' % (self._as, self._greater_equal)
            elif isinstance(self._less, (Param, Table)):
                output = u'%s < %s' % (self._as, self._less)
            elif isinstance(self._less_equal, (Param, Table)):
                output = u'%s <= %s' % (self._as, self._less_equal)
            else:
                output = u'%s AS %s' % (output, self._as)

        return output


class COUNT(Aggregate):
    TYPE = u'COUNT'


class SUM(Aggregate):
    TYPE = u'SUM'
