from datetime import datetime

from pydantic import Field, EmailStr

from ..base_schemas import CamelSerializerModel, CamelAliasModel


class TokenPair(CamelSerializerModel):
    access_token: str
    refresh_token: str


class AccessToken(CamelSerializerModel):
    access_token: str


class RefreshToken(CamelAliasModel):
    refresh_token: str


class UserSchema(CamelSerializerModel):
    id: int
    username: str = Field(..., min_length=2, max_length=150)
    email: EmailStr = Field(..., max_length=254)
    first_name: str | None = Field(None, max_length=150)
    last_name: str | None = Field(None, max_length=150)
    is_superuser: bool
    is_staff: bool
    date_join: datetime


class UserCredentialsSchema(CamelAliasModel):
    username: str = Field(..., max_length=150)
    password: str = Field(..., max_length=128)


class UserCreateSchema(CamelAliasModel):
    username: str = Field(..., min_length=2, max_length=150)
    email: EmailStr = Field(..., max_length=254)
    password: str = Field(..., min_length=8, max_length=50)
    first_name: str | None = Field(None, max_length=150)
    last_name: str | None = Field(None, max_length=150)
