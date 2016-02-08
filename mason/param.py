from __future__ import absolute_import, unicode_literals

from mason.base import Base


class Param(Base):
    def __init__(self, arg):
        self.arg = arg

    def _to_string(self):
        return '%%(%s)s' % self.arg


class ANY(Param):
    def _to_string(self):
        return 'ANY(%s)' % self.arg


class COALESCE(Param):
    def __init__(self, arg, default_value):
        super(COALESCE, self).__init__(arg)
        self.default_value = default_value

    def _to_string(self):
        return 'COALESCE(%s, %s)' % (self.arg, self.default_value)
