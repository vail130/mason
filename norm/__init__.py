from __future__ import absolute_import, unicode_literals

#  _   _
# | \ | |
# |  \| | ___  _ __ _ __ ___
# | . ` |/ _ \| '__| '_ ` _ \
# | |\  | (_) | |  | | | | | |
# \_| \_/\___/|_|  |_| |_| |_|


"""
Norm SQL Generation Library
~~~~~~~~~~~~~~~~~~~~~
Norm is a Python library for generating SQL without an ORM.

:copyright: (c) 2016 Vail Gold.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'norm'
__version__ = '0.1.0'
__author__ = 'Vail Gold'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Vail Gold'

from .aggregate import COUNT, SUM, MAX, MIN
from .conditional import AND, OR, CASE
from .data_type import DATE, TIMESTAMP, DECIMAL, INTEGER, NUMERIC, INTERVAL
from .query.select import SELECT
from .query.update import UPDATE
from .param import Param, ANY, COALESCE
from .table import Table
