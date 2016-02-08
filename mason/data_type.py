from __future__ import absolute_import, unicode_literals

from mason.base import Base


class DataType(Base):
    TYPE = None

    def __init__(self, field, *args):
        self.field = field
        self.args = args

    def _to_string(self):
        output = '(%s)::%s' % (self.field, self.TYPE)
        if self.args:
            output = '%s(%s)' % (output, ', '.join(['%s' % a for a in self.args]))
        return output


class DATE(DataType):
    TYPE = 'DATE'


class TIMESTAMP(DataType):
    TYPE = 'TIMESTAMP'


class INTERVAL(DataType):
    TYPE = 'INTERVAL'


class NUMERIC(DataType):
    TYPE = 'NUMERIC'


class DECIMAL(DataType):
    TYPE = 'DECIMAL'


class INTEGER(DataType):
    TYPE = 'INTEGER'
