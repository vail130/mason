# Norm ![Build Status](https://travis-ci.org/vail130/norm.svg?branch=master)

Norm is a nice, light-weight, SQL query generator. It lets you use objects instead of SQL strings without
having an ORM take over your database model.

## Example
```python
# Annoying
query = """
SELECT purchases.id,
    purchases.product_name,
    (purchases.product_price)::NUMERIC(10, 2),
    (purchases.datetime_purchased)::DATE
FROM purchases
INNER JOIN users ON purchases.purchaser_id = users.user_id
WHERE purchases.datetime_purchased BETWEEN %(start)s AND %(end)s 
    AND (purchases.purchaser_id = %(user_id)s OR purchases.purchaser_id IS NULL)
ORDER BY purchases.datetime_purchased ASC
LIMIT 10
OFFSET 10
"""

# Easy :)
from norm import Table, Param, SELECT, AND, OR, DATE, NUMERIC

purchases = Table('purchases')
users = Table('users')
user_id = Param('user_id')
start = Param('start')
end = Param('end')

query = str(
    SELECT(purchases.id, purchases.product_name, NUMERIC(purchases.product_price, 10, 2),
           DATE(purchases.datetime_purchased))
        .FROM(purchases)
        .INNER_JOIN(users.ON(purchases.purchaser_id == users.user_id))
        .WHERE(AND(purchases.datetime_purchased.BETWEEN(start).AND(end),
                   OR(purchases.purchaser_id == user_id,
                      purchases.purchaser_id.IS_NULL)))
        .ORDER_BY(purchases.datetime_purchased.ASC)
        .LIMIT(10)
        .OFFSET(10)
)
```

## Install
```sh
cd path/to/repos
git clone git@github.com:vail130/norm.git
cd norm
mkvirtualenv norm
pip install -r requirements.txt
```

## Run Tests
```
make test
```
