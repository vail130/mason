Norm
====

Norm is a nice, light-weight, SQL query generator. It lets you use objects instead of SQL strings without
having an ORM take over your database model.

Example
-------
```python
# Painful...
query = """
    SELECT id, product_name, product_price
    FROM purchases
    WHERE datetime_purchased BETWEEN TIMESTAMP '2016-01-01' AND TIMESTAMP '2016-01-02 23:59:59.999999'
    AND (purchaser_id = %(user_id)s OR purchaser_id IS NULL)
    ORDER BY datetime_purchased ASC
"""

# Easy :)
from datetime import datetime

from norm import Table, Param, SELECT, AND, OR

p = Table('purchases')
u = Param('user_id')

query = str(
    SELECT(p.id, p.product_name, p.product_price)
    .FROM(p)
    .WHERE(
        p.datetime_purchased.BETWEEN(datetime(2016, 1, 1), datetime(2016, 1, 2, 23, 59, 59, 999999)),
        AND(p.purchaser_id == u, OR(p.purchaser_id is None)
    ).ORDER_BY(p.datetime_purchased).ASC()
)
```
