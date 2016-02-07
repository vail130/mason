from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base


class Condition(Base):
    CONDITION = None

    def __init__(self, *args):
        if self.CONDITION is None:
            raise NotImplementedError()

        if not args:
            raise NotImplementedError()

        self.conditions = args

    def _to_string(self, nest_level=0):
        condition_strings = []
        for c in self.conditions:
            if isinstance(c, Condition):
                condition_strings.append(c._to_string(nest_level=nest_level + 1))
            else:
                condition_strings.append(unicode(c))

        join_string = u' %s ' % self.CONDITION
        output = join_string.join(condition_strings)

        if nest_level and len(self.conditions) > 1:
            output = u'(%s)' % output

        return output


class AND(Condition):
    CONDITION = u'AND'


class OR(Condition):
    CONDITION = u'OR'


class CASE(Base):
    @classmethod
    def WHEN(cls, condition):
        return cls(condition)

    def __init__(self, condition):
        self.condition = condition
        self.positive = None
        self.negative = None

    def THEN(self, positive):
        self.positive = positive
        return self

    def ELSE(self, negative):
        self.negative = negative
        return self

    @property
    def END(self):
        return self

    def _to_string(self):
        return u'CASE WHEN %s THEN %s ELSE %s END' % (self.condition, self.positive, self.negative)
