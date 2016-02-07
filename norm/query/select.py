from __future__ import absolute_import, unicode_literals

from norm.query.base import Query
from norm.sub_query import SubQuery


class SELECT(Query):
    def __init__(self, *args):
        self._select = args

        self._from = None
        self._joins = []
        self._where = None
        self._group_by = None
        self._having = None
        self._order_by = None
        self._limit = None
        self._offset = None
        self._as = None

    def AS(self, alias):
        return SubQuery(alias, self)

    def FROM(self, *args):
        self._from = args
        return self

    def INNER_JOIN(self, join):
        self._joins.append(('INNER', join))
        return self

    def OUTER_JOIN(self, join):
        self._joins.append(('OUTER', join))
        return self

    def FULL_OUTER_JOIN(self, join):
        self._joins.append(('FULL OUTER', join))
        return self

    def LEFT_OUTER_JOIN(self, join):
        self._joins.append(('LEFT OUTER', join))
        return self

    def RIGHT_OUTER_JOIN(self, join):
        self._joins.append(('RIGHT OUTER', join))
        return self

    def WHERE(self, *args):
        self._where = args
        return self

    def GROUP_BY(self, *args):
        self._group_by = args
        return self

    def HAVING(self, *args):
        self._having = args
        return self

    def ORDER_BY(self, *args):
        self._order_by = args
        return self

    def LIMIT(self, limit):
        if not isinstance(limit, int):
            raise ValueError('LIMIT must be an integer, got "%s"' % limit)

        self._limit = limit
        return self

    def OFFSET(self, offset):
        if not isinstance(offset, int):
            raise ValueError('OFFSET must be an integer, got "%s"' % offset)

        self._offset = offset
        return self

    def _to_string(self, nest_level=0):
        indent = '\t' * nest_level
        sections = [
            indent + 'SELECT %s' % ', '.join([unicode(s) for s in self._select]),
            indent + 'FROM %s' % ', '.join([unicode(s) for s in self._from]),
        ]

        if self._joins:
            for join in self._joins:
                sections.append(
                    indent + '%s JOIN %s' % (join[0], join[1])
                )

        if self._where is not None:
            sections.append(
                indent + 'WHERE %s' % ' '.join([unicode(s) for s in self._where])
            )

        if self._group_by is not None:
            sections.append(
                indent + 'GROUP BY %s' % ', '.join([unicode(s) for s in self._group_by])
            )

        if self._having is not None:
            sections.append(
                indent + 'HAVING %s' % ' '.join([unicode(s) for s in self._having])
            )

        if self._order_by is not None:
            sections.append(
                indent + 'ORDER BY %s' % ' '.join([unicode(s) for s in self._order_by])
            )

        if self._limit is not None:
            sections.append(
                indent + 'LIMIT %s' % self._limit
            )

            if self._offset is not None:
                sections.append(
                    indent + 'OFFSET %s' % self._offset
                )

        return '\n'.join(sections)
