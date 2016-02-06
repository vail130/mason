class Base(object):
    def __unicode__(self):
        return u'%s' % (self.to_string(),)

    def __str__(self):
        return str(self.to_string())

    def to_string(self):
        raise NotImplementedError()


class Table(Base):
    def __init__(self, name, column=None, subquery=None):
        self.name = name
        self.column = column
        self.subquery = subquery

        self._between_start = None
        self._between_end = None
        self._in = None
        self._as = None
        self._on = None
        self._equal = None
        self._greater = None
        self._greater_equal = None
        self._less = None
        self._less_equal = None
        self._is_null = False
        self._is_not_null = False
        self._asc = False
        self._desc = False

    def __getattr__(self, item):
        return Table(self.name, column=item)

    def __eq__(self, other):
        self._equal = other
        return self

    def __gt__(self, other):
        self._greater = other
        return self

    def __ge__(self, other):
        self._greater_equal = other
        return self

    def __lt__(self, other):
        self._less = other
        return self

    def __le__(self, other):
        self._less_equal = other
        return self

    def BETWEEN(self, start):
        if not isinstance(start, Param):
            raise NotImplementedError()

        self._between_start = start
        return self

    def IN(self, arg):
        self._in = arg
        return self

    def AND(self, end):
        if not isinstance(end, Param):
            raise NotImplementedError()

        if not self._between_start:
            raise NotImplementedError()

        self._between_end = end
        return self

    def AS(self, alias):
        self._as = alias
        return self

    def ON(self, *args):
        self._on = args
        return self

    @property
    def IS_NULL(self):
        if self._is_not_null:
            raise NotImplementedError()

        self._is_null = True
        return self

    @property
    def IS_NOT_NULL(self):
        if self._is_null:
            raise NotImplementedError()

        self._is_not_null = True
        return self

    @property
    def ASC(self):
        if self._desc:
            raise NotImplementedError()

        self._asc = True
        return self

    @property
    def DESC(self):
        if self._asc:
            raise NotImplementedError()

        self._desc = True
        return self

    def to_string(self):
        if self._between_start and not self._between_end:
            raise NotImplementedError()

        output = u'%s' % self.name

        if self.column:
            output = u'%s.%s' % (output, self.column)
        elif self.subquery is not None:
            output = u'(\n%s\n) AS %s' % (self.subquery.to_string(nest_level=1), output)

        # Mutually exclusive cases
        if self._as is not None:
            output = u'%s AS %s' % (output, self._as)
        elif self._on is not None:
            output = u'%s ON' % output
            for on in self._on:
                output = u'%s %s' % (output, on)
        elif self._in is not None:
            if isinstance(self._in, SELECT):
                output = u'%s IN (\n%s\n)' % (output, self._in.to_string(nest_level=1))
            else:
                output = u'%s IN (%s)' % (output, self._in)
        elif self._between_start and self._between_end:
            output = u'%s BETWEEN %s AND %s' % (output, self._between_start, self._between_end)
        elif isinstance(self._equal, (Param, Table)):
            output = u'%s = %s' % (output, self._equal)
        elif isinstance(self._greater, (Param, Table)):
            output = u'%s > %s' % (output, self._equal)
        elif isinstance(self._greater_equal, (Param, Table)):
            output = u'%s >= %s' % (output, self._equal)
        elif isinstance(self._less, (Param, Table)):
            output = u'%s < %s' % (output, self._equal)
        elif isinstance(self._less_equal, (Param, Table)):
            output = u'%s <= %s' % (output, self._equal)
        elif self._is_null:
            output = u'%s IS NULL' % output
        elif self._is_not_null:
            output = u'%s IS NOT NULL' % output
        elif self._asc:
            output = u'%s ASC' % output
        elif self._desc:
            output = u'%s DESC' % output

        return output


class Param(Base):
    def __init__(self, name):
        self.name = name

    def to_string(self):
        return u'%(' + unicode(self.name) + u')s'


class ANY(Param):
    def to_string(self):
        return u'ANY(%s)' % self.name


class Condition(Base):
    CONDITION = None

    def __init__(self, *args):
        if self.CONDITION is None:
            raise NotImplementedError()

        if not args:
            raise NotImplementedError()

        self.conditions = args

    def to_string(self, nest_level=0):
        condition_strings = []
        for c in self.conditions:
            if isinstance(c, Condition):
                condition_strings.append(c.to_string(nest_level=nest_level+1))
            else:
                condition_strings.append(unicode(c))

        join_string = u' %s ' % self.CONDITION
        output = join_string.join(condition_strings)

        if nest_level and len(self.conditions) > 1:
            output = u'(%s)' % output

        return output


class AND(Condition):
    CONDITION = u'AND'


class OR(Condition):
    CONDITION = u'OR'


class Aggregate(Base):
    TYPE = None

    def __init__(self, field, **kwargs):
        if self.TYPE is None:
            raise NotImplementedError()

        if not field:
            raise NotImplementedError()

        self.field = field
        self._as = kwargs.get('_as')
        self._equal = kwargs.get('_equal')
        self._greater = kwargs.get('_greater')
        self._greater_equal = kwargs.get('_greater_equal')
        self._less = kwargs.get('_less')
        self._less_equal = kwargs.get('_less_equal')

    def AS(self, alias):
        self._as = alias
        return self

    def __eq__(self, other):
        return self.__class__(self.field, _as=self._as, _equal=other)

    def __gt__(self, other):
        return self.__class__(self.field, _as=self._as, _greater=other)

    def __ge__(self, other):
        return self.__class__(self.field, _as=self._as, _greater_equal=other)

    def __lt__(self, other):
        return self.__class__(self.field, _as=self._as, _less=other)

    def __le__(self, other):
        return self.__class__(self.field, _as=self._as, _less_equal=other)

    def to_string(self):
        if not isinstance(self.field, Table):
            raise NotImplementedError()

        if not self.field.column:
            output = u'%s(*)' % self.TYPE
        else:
            output = u'%s(%s)' % (self.TYPE, self.field)

        if self._as is not None:
            if isinstance(self._equal, (Param, Table)):
                output = u'%s = %s' % (self._as, self._equal)
            elif isinstance(self._greater, (Param, Table)):
                output = u'%s > %s' % (self._as, self._greater)
            elif isinstance(self._greater_equal, (Param, Table)):
                output = u'%s >= %s' % (self._as, self._greater_equal)
            elif isinstance(self._less, (Param, Table)):
                output = u'%s < %s' % (self._as, self._less)
            elif isinstance(self._less_equal, (Param, Table)):
                output = u'%s <= %s' % (self._as, self._less_equal)
            else:
                output = u'%s AS %s' % (output, self._as)

        return output


class COUNT(Aggregate):
    TYPE = u'COUNT'


class SUM(Aggregate):
    TYPE = u'SUM'


class SELECT(Base):
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
        return Table(alias, subquery=self)

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

    def to_string(self, nest_level=0):
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
