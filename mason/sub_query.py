from __future__ import absolute_import, unicode_literals

from mason.base import Base
from mason.column import Column


class SubQuery(Base):
    def __init__(self, name, subquery):
        super(SubQuery, self).__init__()
        self._name = name
        self._subquery = subquery

        self._on = None

    def __getattr__(self, item):
        return Column(item, subquery=self)

    def ON(self, *args):
        self._on = args
        return self

    def _to_string(self):
        output = '(\n%s\n) AS %s' % (self._subquery._to_string(nest_level=1), self._name)

        if self._on is not None:
            output = '%s ON' % output
            for on in self._on:
                output = '%s %s' % (output, on)

        return output
