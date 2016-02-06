from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base

__ALL__ = ['NUMERIC', 'DATE', 'TIMESTAMP', 'DECIMAL', 'INTEGER']


class DataType(Base):
    TYPE = None

    def __init__(self, field, *args):
        self.field = field
        self.args = args

    def to_string(self):
        output = u'(%s)::%s' % (self.field, self.TYPE)
        if self.args:
            output = u'%s(%s)' % (output, u', '.join([unicode(a) for a in self.args]))
        return output


class DATE(DataType):
    TYPE = u'DATE'


class TIMESTAMP(DataType):
    TYPE = u'TIMESTAMP'


class NUMERIC(DataType):
    TYPE = u'NUMERIC'


class DECIMAL(DataType):
    TYPE = u'DECIMAL'


class INTEGER(DataType):
    TYPE = u'INTEGER'
