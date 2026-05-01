from typing import Final, Generic, List, Literal, Optional, Text, TypeVar

from pydantic import BaseModel, Field

__version__: Final[Text] = "0.1.0"

PydnaticModelT = TypeVar("PydnaticModelT", bound=BaseModel)
IdT = TypeVar("IdT")


class Paginatic(BaseModel, Generic[PydnaticModelT, IdT]):
    object: Literal["list"] = Field(default="list", description="The type of object")
    data: List[PydnaticModelT] = Field(..., description="The data of the list")
    first_id: Optional[IdT] = Field(
        default=None, description="The first ID of the list"
    )
    last_id: Optional[IdT] = Field(default=None, description="The last ID of the list")
    has_more: bool = Field(default=False, description="Whether there are more items")
