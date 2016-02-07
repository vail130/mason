from __future__ import absolute_import, unicode_literals

from norm.base import Base


class Assignment(Base):
    def __init__(self, table_name, column_name, value):
        self._table_name = table_name
        self._column_name = column_name
        self._value = value

    def _to_string(self):
        return '%s.%s = %s' % (self._table_name, self._column_name, self._value)
