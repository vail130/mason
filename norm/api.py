class Base(object):
    def __unicode__(self):
        return u'%s' % (self.to_string(),)

    def __str__(self):
        return str(self.to_string())

    def to_string(self):
        raise NotImplementedError()


class Table(Base):
    def __init__(self, name, column=None):
        self.name = name
        self.column = column

        self._between_start = None
        self._between_end = None
        self._as = None
        self._equal = None
        self._is_null = False
        self._is_not_null = False
        self._asc = False
        self._desc = False

    def __getattr__(self, item):
        return Table(self.name, column=item)

    def __eq__(self, other):
        self._equal = other
        return self

    def BETWEEN(self, start):
        if not isinstance(start, Param):
            raise NotImplementedError()

        self._between_start = start
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
        output = '%s' % self.name

        if self.column:
            output = '%s.%s' % (output, self.column)

        if self._as:
            output = '%s AS %s' % (output, self._as)

        # TODO: Not valid with _as
        if self._between_start and not self._between_end:
            raise NotImplementedError()
        elif self._between_start and self._between_end:
            output = '%s BETWEEN %s AND %s' % (output, self._between_start, self._between_end)
        elif isinstance(self._equal, Param):
            output = '%s = %s' % (output, self._equal)
        elif self._is_null:
            output = '%s IS NULL' % output
        elif self._is_not_null:
            output = '%s IS NOT NULL' % output
        elif self._asc:
            output = '%s ASC' % output
        elif self._desc:
            output = '%s DESC' % output

        return output


class Param(Base):
    def __init__(self, name):
        self.name = name

    def to_string(self):
        return '%(' + self.name + ')s'


class Condition(Base):
    CONDITION = None

    def __init__(self, *args):
        if self.CONDITION is None:
            raise NotImplementedError()

        if not args:
            raise NotImplementedError()

        self.conditions = args

    def to_string(self):
        output = self.CONDITION
        condition_string = ' '.join([str(c) for c in self.conditions])

        if len(self.conditions) == 1:
            return '%s %s' % (output, condition_string)
        else:
            return '%s (%s)' % (output, condition_string)


class AND(Condition):
    CONDITION = 'AND'


class OR(Condition):
    CONDITION = 'OR'


class SELECT(Base):
    def __init__(self, *args):
        self._select = args

        self._from = None
        self._where = None
        self._group_by = None
        self._having = None
        self._order_by = None
        self._limit = None

    def FROM(self, *args):
        self._from = args
        return self

    def WHERE(self, *args):
        self._where = args
        return self

    def ORDER_BY(self, *args):
        self._order_by = args
        return self

    def LIMIT(self, *args):
        self._limit = args
        return self

    def to_string(self):
        sections = [
            'SELECT %s' % ', '.join([str(s) for s in self._select]),
            'FROM %s' % ', '.join([str(s) for s in self._from]),
        ]

        if self._where is not None:
            sections.append(
                'WHERE %s' % ' '.join([str(s) for s in self._where])
            )

        if self._order_by is not None:
            sections.append(
                'ORDER BY %s' % ' '.join([str(s) for s in self._order_by])
            )

        return '\n'.join(sections)
