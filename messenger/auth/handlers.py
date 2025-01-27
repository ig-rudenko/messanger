from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .jwt import create_jwt_token_pair, refresh_access_token
from .models import User
from .users import create_user, get_user_by_credentials, get_current_user
from ..orm.session_manager import get_session
from .schemas import (
    TokenPair,
    RefreshToken,
    AccessToken,
    UserSchema,
    UserCreateSchema,
    UserCredentialsSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/users", response_model=UserSchema)
async def register_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """Регистрация нового пользователя"""
    return await create_user(session, user)


@router.post("/token", response_model=TokenPair)
async def get_tokens(user_data: UserCredentialsSchema, session: AsyncSession = Depends(get_session)):
    """Получение пары JWT"""
    user = await get_user_by_credentials(session, user_data.username, user_data.password)
    return create_jwt_token_pair(user_id=user.id)


@router.post("/token/refresh", response_model=AccessToken)
def refresh_token(token: RefreshToken):
    """Получение нового access token через refresh token"""
    return AccessToken(access_token=refresh_access_token(token.refresh_token))


@router.get("/myself", response_model=UserSchema)
def verify_jwt(user: User = Depends(get_current_user)):
    """Проверка JWT"""
    return user
