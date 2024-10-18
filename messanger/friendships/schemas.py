from typing import Optional

from pydantic import Field, BaseModel

from ..base_schemas import CamelSerializerModel


class FriendshipEntitySchema(CamelSerializerModel):
    id: int
    type: str
    username: str
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class ExistingFriendshipEntitySchema(FriendshipEntitySchema):
    last_message: Optional[str] = Field(default=None)
    last_datetime: Optional[int] = Field(default=None)
    online: bool = Field(default=False)


class NewFriendshipEntitySchema(BaseModel):
    username: str
