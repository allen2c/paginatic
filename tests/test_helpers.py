"""Tests for pagination token helpers."""

from typing import Text

import pytest

from paginatic.helpers import decode_and_verify, encode_and_sign

SECRET: Text = "test-secret"


def test_encode_and_sign_round_trips_payload():
    payload = {
        "created_at": "2026-05-01T10:30:00Z",
        "id": "item_123",
        "sort": "created_at_desc",
        "version": 1,
    }

    token = encode_and_sign(payload, secret=SECRET)

    assert decode_and_verify(token, secret=SECRET) == payload


def test_encode_and_sign_returns_urlsafe_opaque_text():
    token = encode_and_sign({"id": "item_123"}, secret=SECRET)

    assert isinstance(token, str)
    assert "." in token
    assert "=" not in token


def test_encode_and_sign_is_stable_for_equivalent_payload_order():
    first_token = encode_and_sign({"id": "item_123", "version": 1}, secret=SECRET)
    second_token = encode_and_sign({"version": 1, "id": "item_123"}, secret=SECRET)

    assert first_token == second_token


def test_decode_and_verify_rejects_tampered_payload():
    token = encode_and_sign({"id": "item_123"}, secret=SECRET)
    payload_part, signature = token.split(".", maxsplit=1)
    tampered_token = ".".join([f"{payload_part}a", signature])

    with pytest.raises(ValueError, match="signature"):
        decode_and_verify(tampered_token, secret=SECRET)


def test_decode_and_verify_rejects_wrong_secret():
    token = encode_and_sign({"id": "item_123"}, secret=SECRET)

    with pytest.raises(ValueError, match="signature"):
        decode_and_verify(token, secret="other-secret")


def test_decode_and_verify_rejects_malformed_token():
    with pytest.raises(ValueError, match="Invalid pagination token"):
        decode_and_verify("not-a-signed-token", secret=SECRET)


def test_encode_and_sign_requires_secret():
    with pytest.raises(ValueError, match="signing secret"):
        encode_and_sign({"id": "item_123"}, secret="")


def test_decode_and_verify_requires_secret():
    token = encode_and_sign({"id": "item_123"}, secret=SECRET)

    with pytest.raises(ValueError, match="signing secret"):
        decode_and_verify(token, secret="")
