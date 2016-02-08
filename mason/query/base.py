from __future__ import absolute_import, unicode_literals

from mason.base import Base


class Query(Base):
    def _to_string(self, nest_level=0):
        raise NotImplementedError()
