from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base


class Param(Base):
    def __init__(self, arg):
        self.arg = arg

    def _to_string(self):
        return u'%(' + unicode(self.arg) + u')s'


class ANY(Param):
    def _to_string(self):
        return u'ANY(%s)' % self.arg


class COALESCE(Param):
    def __init__(self, arg, default_value):
        super(COALESCE, self).__init__(arg)
        self.default_value = default_value

    def __getattr__(self, item):
        return getattr(self.arg, item)

    def _to_string(self):
        return u'COALESCE(%s, %s)' % (self.arg, self.default_value)
