# Paginatic

Paginatic is a small set of Pydantic models for API pagination responses.

It supports two common pagination styles:

- ID cursor pagination with `first_id`, `last_id`, and `has_more`
- Token pagination with `next_page_token`

## Install

```bash
pip install paginatic
```

## Basic Usage

```python
from typing import Text

from pydantic import BaseModel

from paginatic import Paginatic


class User(BaseModel):
    id: Text
    name: Text


page = Paginatic[User, Text](
    data=[
        User(id="user_1", name="Ada"),
        User(id="user_2", name="Grace"),
    ],
    first_id="user_1",
    last_id="user_2",
    has_more=True,
)

print(page.model_dump())
```

Output:

```json
{
  "object": "list",
  "data": [
    {"id": "user_1", "name": "Ada"},
    {"id": "user_2", "name": "Grace"}
  ],
  "first_id": "user_1",
  "last_id": "user_2",
  "has_more": true
}
```

## Token Pagination

```python
from paginatic import TokenPaginatic

page = TokenPaginatic[User](
    data=[User(id="user_1", name="Ada")],
    next_page_token="opaque-token",
)
```

Use token pagination when the next page is represented by an opaque server-generated token.

## Helpers

```python
from paginatic.helpers import decode_and_verify, encode_and_sign

secret = "replace-me"

token = encode_and_sign(
    {
        "created_at": "2026-05-01T10:30:00Z",
        "id": "user_2",
        "sort": "created_at_desc",
        "version": 1,
    },
    secret=secret,
)

payload = decode_and_verify(token, secret=secret)
```

Tokens are signed, not encrypted. Do not put secrets or private user data in token payloads.
