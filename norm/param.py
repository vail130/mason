from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base


class Param(Base):
    def __init__(self, name):
        self.name = name

    def to_string(self):
        return u'%(' + unicode(self.name) + u')s'


class ANY(Param):
    def to_string(self):
        return u'ANY(%s)' % self.name
