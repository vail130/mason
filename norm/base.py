from __future__ import absolute_import
from __future__ import print_function


class Base(object):
    def __unicode__(self):
        return u'%s' % (self._to_string(),)

    def __str__(self):
        return str(self._to_string())

    def _to_string(self):
        raise NotImplementedError()
