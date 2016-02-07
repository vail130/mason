from __future__ import absolute_import, unicode_literals

from norm.base import Base


class UPDATE(Base):
    def __init__(self, arg):
        self._update = arg

        self._set = None
        self._from = None
        self._where = None

    def SET(self, **kwargs):
        self._set = kwargs
        return self

    def FROM(self, *args):
        self._from = args
        return self

    def WHERE(self, *args):
        self._where = args
        return self

    def _to_string(self):
        set_expressions = []
        for k, v in self._set.iteritems():
            set_expressions.append('%s.%s = %s' % (self._update, k, v))

        sections = [
            'UPDATE %s' % self._update,
            'SET %s' % ', '.join(set_expressions),
        ]

        if self._from is not None:
            sections.append(
                'FROM %s' % ' '.join([unicode(s) for s in self._from])
            )

        if self._where is not None:
            sections.append(
                'WHERE %s' % ' '.join([unicode(s) for s in self._where])
            )

        return '\n'.join(sections)
