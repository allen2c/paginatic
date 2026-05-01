# API Reference

## `Paginatic`

```python
class Paginatic(BaseModel, Generic[PydanticModelT, IdT])
```

ID cursor pagination response model.

Fields:

- `object: Literal["list"]`
- `data: List[PydanticModelT]`
- `first_id: Optional[IdT]`
- `last_id: Optional[IdT]`
- `has_more: bool`

## `TokenPaginatic`

```python
class TokenPaginatic(BaseModel, Generic[PydanticModelT])
```

Token pagination response model.

Fields:

- `object: Literal["list"]`
- `data: List[PydanticModelT]`
- `next_page_token: Optional[Text]`

## `encode_and_sign`

```python
def encode_and_sign(payload: Mapping[Text, Any], secret: Text) -> Text
```

Encode a JSON payload and sign it with HMAC-SHA256.

Raises:

- `ValueError` when `secret` is empty

## `decode_and_verify`

```python
def decode_and_verify(token: Text, secret: Text) -> dict[Text, Any]
```

Decode a token after verifying its HMAC-SHA256 signature.

Raises:

- `ValueError` when `secret` is empty
- `ValueError` when the token is malformed
- `ValueError` when the token signature is invalid
- `ValueError` when the token payload is invalid
