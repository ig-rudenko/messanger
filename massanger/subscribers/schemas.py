from pydantic import Field
from ..base_schemas import CamelAliasModel


class SubscriberSchema(CamelAliasModel):
    id: int
    username: str
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
