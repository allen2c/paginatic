"""Helpers for building opaque pagination tokens."""

import base64
import binascii
import hashlib
import hmac
import json
from typing import Any, Final, Mapping, Text

__all__ = ["decode_and_verify", "encode_and_sign"]

TOKEN_SEPARATOR: Final[Text] = "."


def encode_and_sign(payload: Mapping[Text, Any], secret: Text) -> Text:
    """Encode a JSON payload and sign it with HMAC-SHA256."""
    _ensure_secret(secret)

    payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    payload_part = _base64url_encode(payload_json.encode())
    signature = _sign(payload_part, secret)

    return TOKEN_SEPARATOR.join([payload_part, signature])


def decode_and_verify(token: Text, secret: Text) -> dict[Text, Any]:
    """Decode a signed token after verifying its HMAC-SHA256 signature."""
    _ensure_secret(secret)

    try:
        payload_part, signature = token.split(TOKEN_SEPARATOR, maxsplit=1)
    except ValueError as exc:
        raise ValueError("Invalid pagination token") from exc

    expected_signature = _sign(payload_part, secret)
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid pagination token signature")

    try:
        payload_json = _base64url_decode(payload_part).decode()
        payload = json.loads(payload_json)
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid pagination token payload") from exc

    if not isinstance(payload, dict):
        raise ValueError("Invalid pagination token payload")

    return payload


def _base64url_encode(value: bytes) -> Text:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _base64url_decode(value: Text) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _ensure_secret(secret: Text) -> None:
    if not secret:
        raise ValueError("A signing secret is required")


def _sign(payload_part: Text, secret: Text) -> Text:
    signature = hmac.new(
        key=secret.encode(),
        msg=payload_part.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    return _base64url_encode(signature)
