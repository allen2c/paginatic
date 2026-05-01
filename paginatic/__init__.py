from typing import Final, Generic, List, Literal, Optional, Text, TypeVar

from pydantic import BaseModel, Field

__version__: Final[Text] = "0.1.0"

PydanticModelT = TypeVar("PydanticModelT", bound=BaseModel)
IdT = TypeVar("IdT")


class Paginatic(BaseModel, Generic[PydanticModelT, IdT]):
    object: Literal["list"] = Field(default="list", description="The type of object")
    data: List[PydanticModelT] = Field(
        default_factory=list, description="The data of the list"
    )
    first_id: Optional[IdT] = Field(
        default=None, description="The first ID of the list"
    )
    last_id: Optional[IdT] = Field(default=None, description="The last ID of the list")
    has_more: bool = Field(default=False, description="Whether there are more items")


class TokenPaginatic(BaseModel, Generic[PydanticModelT]):
    object: Literal["list"] = Field(default="list", description="The type of object")
    data: List[PydanticModelT] = Field(
        default_factory=list, description="The data of the list"
    )
    next_page_token: Optional[Text] = Field(default=None, description="The token")
