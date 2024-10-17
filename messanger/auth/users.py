import re
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from ..orm.session_manager import get_session
from .schemas import UserCreateSchema
from .encrypt import encrypt_password, validate_password
from .exc import CredentialsException
from .jwt import oauth2_scheme, _get_token_payload, USER_IDENTIFIER


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session, use_cache=True),
) -> User:
    """
    Получение текущего пользователя по токену аутентификации.

    :param token: Токен пользователя.
    :param session: :class:`AsyncSession` объект сессии.
    :return: Объект пользователя :class:`User`.
    :raises CredentialsException: Если пользователь не найден.
    """
    payload = _get_token_payload(token, "access")
    try:
        user = await User.get(session, id=payload[USER_IDENTIFIER])
    except NoResultFound:
        raise CredentialsException

    return user


async def get_user_or_none(
    authorization: Optional[str] = Header(None),
    session: AsyncSession = Depends(get_session, use_cache=True),
) -> User | None:
    """
    Получение текущего пользователя по токену аутентификации.

    :param authorization: Значение заголовка HTTP (Authorization).
    :param session: :class:`AsyncSession` объект сессии.
    :return: Объект пользователя :class:`User` или :class:`None`.
    :raises CredentialsException: Если пользователь не найден.
    """
    if authorization:
        if token_match := re.match(r"Bearer (\S+)", authorization):
            try:
                return await get_current_user(token_match.group(1), session)
            except HTTPException:
                return None
    return None


async def create_user(session: AsyncSession, user: UserCreateSchema) -> User:
    obj = User(
        username=user.username,
        email=user.email,
        password=encrypt_password(user.password),
        last_name=user.last_name,
        first_name=user.first_name,
    )
    session.add(obj)
    try:
        await session.commit()
    except IntegrityError as exc:
        if match := re.search(r"UNIQUE constraint failed: users\.(\S+)", str(exc)):
            raise HTTPException(
                status_code=422, detail=f"Пользователь с таким `{match.group(1)}` уже существует"
            )
        raise exc
    else:
        await session.refresh(obj)
        return obj


async def get_user_by_credentials(session: AsyncSession, username: str, password: str) -> User:
    try:
        user_model = await User.get(session, username=username)
    except NoResultFound:
        raise CredentialsException

    if not validate_password(password, user_model.password):
        raise CredentialsException
    return user_model
