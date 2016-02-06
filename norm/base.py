from __future__ import absolute_import
from __future__ import print_function


class Base(object):
    def __unicode__(self):
        return u'%s' % (self.to_string(),)

    def __str__(self):
        return str(self.to_string())

    def to_string(self):
        raise NotImplementedError()
