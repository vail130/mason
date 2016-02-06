Norm
====

Norm is a nice, light-weight, SQL query generator. It lets you use objects instead of SQL strings without
having an ORM take over your database model.

Example
-------
```python
# Annoying
query = """
SELECT purchases.id, purchases.product_name, purchases.product_price
FROM purchases
WHERE purchases.datetime_purchased BETWEEN %(start)s AND %(end)s
    AND (purchases.purchaser_id = %(user_id)s OR purchases.purchaser_id IS NULL)
ORDER BY purchases.datetime_purchased ASC
"""

# Easy :)
from norm import Table, Param, SELECT, AND, OR

p = Table('purchases')
user_id = Param('user_id')
start = Param('start')
end = Param('end')

query = str(
    SELECT(p.id, p.product_name, p.product_price)
        .FROM(p)
        .WHERE(p.datetime_purchased.BETWEEN(start).AND(end),
               AND(p.purchaser_id == user_id, OR(p.purchaser_id.IS_NULL)))
        .ORDER_BY(p.datetime_purchased.ASC)
)
```

Run Tests
---------
```
make test
```
