from datetime import datetime

from pydantic import Field, BaseModel

from ..base_schemas import CamelAliasModel, CamelSerializerModel


class MessageSchema(BaseModel):
    type: str
    status: str
    message: str


class MessageRequestSchema(CamelAliasModel, MessageSchema):
    recipient_id: int | None = Field(None)


class MessageResponseSchema(CamelSerializerModel, MessageSchema):
    recipient_id: int
    sender_id: int
    created_at: int
