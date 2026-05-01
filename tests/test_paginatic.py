"""Tests for the public paginatic models."""

from typing import Text

import pytest
from pydantic import BaseModel, ValidationError

from paginatic import Paginatic, TokenPaginatic, __version__

DEFAULT_VERSION: Text = "0.1.0"


def test_version_matches_package_metadata():
    assert __version__ == DEFAULT_VERSION


def test_paginatic_uses_declared_defaults():
    page = Paginatic[_Item, Text]()

    assert page.object == "list"
    assert page.data == []
    assert page.first_id is None
    assert page.last_id is None
    assert page.has_more is False


def test_paginatic_builds_nested_models_from_mapping_data():
    page = Paginatic[_Item, Text](
        data=[{"id": "item_1", "name": "Alpha"}],
        first_id="item_1",
        last_id="item_1",
        has_more=True,
    )

    assert page.data == [_Item(id="item_1", name="Alpha")]
    assert page.model_dump() == {
        "object": "list",
        "data": [{"id": "item_1", "name": "Alpha"}],
        "first_id": "item_1",
        "last_id": "item_1",
        "has_more": True,
    }


def test_paginatic_supports_non_text_id_types():
    page = Paginatic[_Item, int](
        data=[_Item(id="item_1", name="Alpha")],
        first_id=1,
        last_id=1,
    )

    assert page.first_id == 1
    assert page.last_id == 1


def test_paginatic_data_default_is_not_shared_between_instances():
    first_page = Paginatic[_Item, Text]()
    second_page = Paginatic[_Item, Text]()

    first_page.data.append(_Item(id="item_1", name="Alpha"))

    assert first_page.data == [_Item(id="item_1", name="Alpha")]
    assert second_page.data == []


def test_paginatic_requires_list_object_literal():
    with pytest.raises(ValidationError):
        Paginatic[_Item, Text](object="collection")


def test_token_paginatic_uses_declared_defaults():
    page = TokenPaginatic[_Item]()

    assert page.object == "list"
    assert page.data == []
    assert page.next_page_token is None


def test_token_paginatic_serializes_next_page_token():
    page = TokenPaginatic[_Item](
        data=[{"id": "item_1", "name": "Alpha"}],
        next_page_token="page_2",
    )

    assert page.data == [_Item(id="item_1", name="Alpha")]
    assert page.model_dump() == {
        "object": "list",
        "data": [{"id": "item_1", "name": "Alpha"}],
        "next_page_token": "page_2",
    }


class _Item(BaseModel):
    id: Text
    name: Text
