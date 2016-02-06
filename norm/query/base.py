from __future__ import absolute_import
from __future__ import print_function

from norm.base import Base


class Query(Base):
    def to_string(self, nest_level=0):
        raise NotImplementedError()
