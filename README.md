# Paginatic

[![PyPI version](https://img.shields.io/pypi/v/paginatic.svg)](https://pypi.org/project/paginatic/)
[![Python Version](https://img.shields.io/pypi/pyversions/paginatic.svg)](https://pypi.org/project/paginatic/)
[![License](https://img.shields.io/pypi/l/paginatic.svg)](https://opensource.org/licenses/MIT)

Small Pydantic models for API pagination responses.

## Features

- ID cursor pagination with `first_id`, `last_id`, and `has_more`
- Token pagination with `next_page_token`
- Signed opaque page-token helpers
- Pydantic generic models for typed response data

## Installation

```bash
pip install paginatic
```

## Quick Start

```python
from typing import Text

from pydantic import BaseModel

from paginatic import Paginatic, TokenPaginatic


class User(BaseModel):
    id: Text
    name: Text


id_page = Paginatic[User, Text](
    data=[User(id="user_1", name="Ada")],
    first_id="user_1",
    last_id="user_1",
    has_more=False,
)

token_page = TokenPaginatic[User](
    data=[User(id="user_1", name="Ada")],
    next_page_token="opaque-next-page-token",
)
```

## ID Cursor Pagination

Use `Paginatic` when the response exposes item IDs as cursors.

```python
page = Paginatic[User, Text](
    data=[
        {"id": "user_1", "name": "Ada"},
        {"id": "user_2", "name": "Grace"},
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

Use `TokenPaginatic` when the next page is represented by an opaque server-generated token.

```python
from paginatic.helpers import decode_and_verify, encode_and_sign

secret = "replace-me"

next_page_token = encode_and_sign(
    {
        "created_at": "2026-05-01T10:30:00Z",
        "id": "user_2",
        "sort": "created_at_desc",
        "version": 1,
    },
    secret=secret,
)

page = TokenPaginatic[User](
    data=[User(id="user_1", name="Ada"), User(id="user_2", name="Grace")],
    next_page_token=next_page_token,
)

payload = decode_and_verify(next_page_token, secret=secret)
```

Tokens are signed, not encrypted. Do not put secrets or private user data in token payloads.

## Configuration

No configuration is required.

## License

MIT License
