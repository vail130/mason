from norm.base import Base
from norm.column import Column


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
        output = u'(\n%s\n) AS %s' % (self._subquery._to_string(nest_level=1), self._name)

        if self._on is not None:
            output = u'%s ON' % output
            for on in self._on:
                output = u'%s %s' % (output, on)

        return output
