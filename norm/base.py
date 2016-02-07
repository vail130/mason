from __future__ import absolute_import, unicode_literals


class Base(object):
    def __unicode__(self):
        return '%s' % (self._to_string(),)

    def __str__(self):
        return str(self._to_string())

    def _to_string(self):
        raise NotImplementedError()
