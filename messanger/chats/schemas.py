from pydantic import BaseModel


class UpdateLastReadSchema(BaseModel):
    timestamp: int


class LastReadSchema(BaseModel):
    timestamp: int | None
