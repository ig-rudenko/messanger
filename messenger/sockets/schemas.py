from pydantic import Field

from ..base_schemas import CamelAliasModel, CamelSerializerModel


class MessageRequestSchema(CamelAliasModel):
    type: str
    status: str
    message: str
    recipient_id: int | None = Field(None)


class MessageResponseSchema(CamelSerializerModel):
    type: str
    status: str
    message: str
    recipient_id: int
    sender_id: int
    created_at: int
