# Token Helpers

`paginatic.helpers` provides small helpers for signed pagination tokens.

```python
from paginatic.helpers import decode_and_verify, encode_and_sign
```

## Create A Token

```python
secret = "replace-me-with-a-secret-from-your-config"

token = encode_and_sign(
    {
        "created_at": "2026-05-01T10:30:00Z",
        "id": "item_123",
        "sort": "created_at_desc",
        "version": 1,
    },
    secret=secret,
)
```

The token is URL-safe text:

```text
eyJjcmVhdGVkX2F0IjoiMjAyNi0wNS0wMVQxMDozMDowMFoiLCJpZCI6Iml0ZW1fMTIzIiwic29ydCI6ImNyZWF0ZWRfYXRfZGVzYyIsInZlcnNpb24iOjF9.N439w5tMV7FtS0ZatIa0CaeROfFg_YYZEWDQucb7gb0
```

The format is:

```text
base64url_payload.base64url_signature
```

Treat the whole token as opaque in clients.

## Read A Token

```python
payload = decode_and_verify(token, secret=secret)

created_at = payload["created_at"]
item_id = payload["id"]
```

If the token is malformed, signed with a different secret, or changed by the client, `decode_and_verify` raises `ValueError`.

```python
try:
    payload = decode_and_verify(page_token, secret=secret)
except ValueError:
    # Return a 400 Bad Request response from your API layer.
    raise
```

## Server Flow

Typical token pagination flow:

1. Query one extra row.
2. Return only the requested number of rows.
3. If the extra row exists, create `next_page_token` from the last returned row.
4. On the next request, decode and verify `page_token`.
5. Use the decoded cursor values in the next query.

Example payload:

```python
payload = {
    "created_at": last_item.created_at.isoformat(),
    "id": last_item.id,
    "sort": "created_at_desc",
    "version": 1,
}
```

Example SQL shape:

```sql
WHERE (created_at, id) < (:created_at, :id)
ORDER BY created_at DESC, id DESC
LIMIT :limit_plus_one
```

## Security Notes

Tokens are signed, not encrypted.

Good token payloads:

- item ID
- created timestamp
- sort direction
- token version

Avoid putting these in token payloads:

- passwords
- API keys
- private user data
- secrets
