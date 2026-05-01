# Usage

## ID Cursor Pagination

Use `Paginatic` when the response exposes item IDs as cursors.

```python
from typing import Text

from pydantic import BaseModel

from paginatic import Paginatic


class Product(BaseModel):
    id: Text
    name: Text


products = [
    Product(id="product_1", name="Keyboard"),
    Product(id="product_2", name="Mouse"),
]

page = Paginatic[Product, Text](
    data=products,
    first_id=products[0].id,
    last_id=products[-1].id,
    has_more=True,
)
```

This produces:

```json
{
  "object": "list",
  "data": [
    {"id": "product_1", "name": "Keyboard"},
    {"id": "product_2", "name": "Mouse"}
  ],
  "first_id": "product_1",
  "last_id": "product_2",
  "has_more": true
}
```

`IdT` can be any ID type your API uses:

```python
page = Paginatic[Product, int](
    data=products,
    first_id=1,
    last_id=2,
)
```

## Token Pagination

Use `TokenPaginatic` when the next page is represented by a server-generated token.

```python
from paginatic import TokenPaginatic

page = TokenPaginatic[Product](
    data=products,
    next_page_token="opaque-next-page-token",
)
```

This produces:

```json
{
  "object": "list",
  "data": [
    {"id": "product_1", "name": "Keyboard"},
    {"id": "product_2", "name": "Mouse"}
  ],
  "next_page_token": "opaque-next-page-token"
}
```

When there is no next page, leave `next_page_token` as `None`.

```python
page = TokenPaginatic[Product](data=products)
```

## Parsing Mapping Data

Paginatic models keep normal Pydantic parsing behavior.

```python
page = Paginatic[Product, Text](
    data=[
        {"id": "product_1", "name": "Keyboard"},
        {"id": "product_2", "name": "Mouse"},
    ],
    first_id="product_1",
    last_id="product_2",
)

assert page.data == [
    Product(id="product_1", name="Keyboard"),
    Product(id="product_2", name="Mouse"),
]
```
