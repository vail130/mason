from __future__ import absolute_import
from __future__ import print_function

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
        self._joins.append((u'INNER', join))
        return self

    def OUTER_JOIN(self, join):
        self._joins.append((u'OUTER', join))
        return self

    def FULL_OUTER_JOIN(self, join):
        self._joins.append((u'FULL OUTER', join))
        return self

    def LEFT_OUTER_JOIN(self, join):
        self._joins.append((u'LEFT OUTER', join))
        return self

    def RIGHT_OUTER_JOIN(self, join):
        self._joins.append((u'RIGHT OUTER', join))
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
            raise ValueError(u'LIMIT must be an integer, got "%s"' % limit)

        self._limit = limit
        return self

    def OFFSET(self, offset):
        if not isinstance(offset, int):
            raise ValueError(u'OFFSET must be an integer, got "%s"' % offset)

        self._offset = offset
        return self

    def _to_string(self, nest_level=0):
        indent = u'\t' * nest_level
        sections = [
            indent + u'SELECT %s' % u', '.join([unicode(s) for s in self._select]),
            indent + u'FROM %s' % u', '.join([unicode(s) for s in self._from]),
        ]

        if self._joins:
            for join in self._joins:
                sections.append(
                    indent + u'%s JOIN %s' % (join[0], join[1])
                )

        if self._where is not None:
            sections.append(
                indent + u'WHERE %s' % u' '.join([unicode(s) for s in self._where])
            )

        if self._group_by is not None:
            sections.append(
                indent + u'GROUP BY %s' % u', '.join([unicode(s) for s in self._group_by])
            )

        if self._having is not None:
            sections.append(
                indent + u'HAVING %s' % u' '.join([unicode(s) for s in self._having])
            )

        if self._order_by is not None:
            sections.append(
                indent + u'ORDER BY %s' % u' '.join([unicode(s) for s in self._order_by])
            )

        if self._limit is not None:
            sections.append(
                indent + u'LIMIT %s' % self._limit
            )

            if self._offset is not None:
                sections.append(
                    indent + u'OFFSET %s' % self._offset
                )

        return u'\n'.join(sections)
