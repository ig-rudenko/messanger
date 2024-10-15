from pydantic import Field, BaseModel

from ..base_schemas import CamelAliasModel, CamelSerializerModel


class MessageSchema(BaseModel):
    type: str
    status: str
    message: str


class MessageRequestSchema(CamelAliasModel, MessageSchema):
    recipient_username: str | None = Field(None)


class MessageResponseSchema(CamelSerializerModel, MessageSchema):
    recipient_username: str
    sender_username: str
