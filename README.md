```sh
# -- build & start 
docker compose up -d --build

# go to localhost:8000/api/ to see 'Hello!' message
# api routes given below

# -- run unit tests 
docker compose exec backend python manage.py test

# -- stop
docker compose down
```

## Overview
:: Assumptions
- vendors are like regular `Users`, but with `is_seller` as `True`. All users have a `balance`.
- A (monetary) transaction involves exactly one vendor, & one client (who can be any `User`)
- Transaction details already exist in the db, so only the `transaction_id` is sent via http request. 
- A `Transaction` contains an `amount`, along with a `vendor` & `customer` (foreign keys to `User`). Complete model is at `transactions/models.py`

misc. implementation details:
- for convenience, view functions take parameters as url slugs
- data is serialized as json, via `django-rest-framework`
- custom `User` implemented at `accounts/models.py`

:: Routes
- `/api/transactions/` - get all transactions
- `/api/vendors/` - get all vendors
- `/api/transactions/<uuid:vendor_id>` - get transactions for a particular vendor
- `/api/transaction/<uuid:transaction_id>` - perform the transaction with given id. 
- `/api/hello/` - displays a `"Hello!"` message, for debugging

### Handling Race Conditions

Use case - concurrent updates on a vendor's `balance` shouldn't cause write conflicts

:: Possible solutions

i) (Currently implemented) db transactions, via `django.db.transaction`

from `transactions/views.py`:

```py
from django.db import transaction as db_transaction
from .models import Transaction

def perform_payment(request, transaction_id):
    ...
    with db_transaction.atomic():
        vendor = transaction['vendor']
        amount = transaction['amount']
        vendor.balance += amount 
        vendor.save()
    ...
```

ii) db transactions, using [F-expressions](https://docs.djangoproject.com/en/4.0/ref/models/expressions/#f-expressions)

F-expressions translate to direct DB operations,  instead of needing Python to fetch data into memory

```py
from django.db.models import F 
from accounts.models import User

vendor = User.objects.get(id=vendor_id)

# unsafe - could lead to race conditions
vendor.balance += 1
vendor.save()

# safe, with F()
vendor.update(balance = F('balance') + 1)
```

> "Another useful benefit of F() is that having the database - rather than Python - update a field’s value avoids a race condition. <br/> <br />
> If two Python threads execute the code in the first example above, one thread could retrieve, increment, and save a field’s value after the other has retrieved it from the database. The value that the second thread saves will be based on the original value; the work of the first thread will be lost.  - Python docs" <br/>
> \- [Avoiding Race Conditions using F() (Django docs)](https://docs.djangoproject.com/en/4.0/ref/models/expressions/#avoiding-race-conditions-using-f)


<br />

## References
1) Designing Data-Intensive Applications, M. Kleppmann (2017)
2) Django For REST APIs, W Vincent (2022)
3) Django For Professionals, W Vincent (2020)
4) https://tech.serhatteker.com/post/2020-01/email-as-username-django/