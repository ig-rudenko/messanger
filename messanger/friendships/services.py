from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Friendship
from .schemas import FriendshipEntitySchema, ExistingFriendshipEntitySchema
from ..auth.models import User
from ..cache import AbstractCache
from ..chats.messages import get_one_last_message
from ..sockets.schemas import MessageResponseSchema
from ..sockets.status import is_user_online


async def get_my_friendships_data(
    session: AsyncSession, user_id: int, cache: AbstractCache
) -> list[ExistingFriendshipEntitySchema]:

    friendships = await get_user_friendships(session, user_id, cache)

    result = []

    for friendship in friendships:
        last_message: MessageResponseSchema | None = await get_one_last_message(
            session,
            chat_id=friendship.id,
            user_id=user_id,
            cache=cache,
        )
        result.append(
            ExistingFriendshipEntitySchema(
                id=friendship.id,
                type="user",
                username=friendship.username,
                first_name=friendship.first_name,
                last_name=friendship.last_name,
                last_message=last_message.message if last_message else None,
                last_datetime=last_message.created_at if last_message else None,
                online=await is_user_online(friendship.id, cache),
            )
        )
    return result


async def get_user_friendships(
    session: AsyncSession, user_id: int, cache: AbstractCache | None = None
) -> list[FriendshipEntitySchema]:
    cache_key = f"user_friendships:{user_id}"
    if cache is not None:
        cached_friendships: list[FriendshipEntitySchema] | None = await cache.get(cache_key)
        if cached_friendships is not None:
            return cached_friendships

    query = (
        select(User.id, User.username, User.first_name, User.last_name)
        .join(Friendship, Friendship.friend_id == User.id)
        .where(Friendship.user_id == user_id)
    )

    result = await session.execute(query)

    friendships = []
    for row in result:
        friendships.append(
            FriendshipEntitySchema(
                type="user",
                id=row[0],
                username=row[1],
                first_name=row[2],
                last_name=row[3],
            )
        )

    if cache is not None:
        await cache.set(cache_key, friendships, expire=-1)

    return friendships


async def create_friendship(
    session: AsyncSession, user_id: int, friend_username: str, cache: AbstractCache | None = None
) -> FriendshipEntitySchema:
    friend = await User.get(session, username=friend_username)

    save_point = await session.begin_nested()
    session.add(Friendship(user_id=user_id, friend_id=friend.id))

    friendship = FriendshipEntitySchema(
        id=friend.id,
        username=friend.username,
        first_name=friend.first_name,
        last_name=friend.last_name,
        type="user",
    )

    try:
        await save_point.commit()
    except IntegrityError:
        await save_point.rollback()
    else:
        # Добавляем в кэш новую запись.
        cache_key = f"user_friendships:{user_id}"
        cached_friendship: list[FriendshipEntitySchema] = (await cache.get(cache_key)) or []
        cached_friendship.append(friendship)
        await cache.set(cache_key, cached_friendship, expire=-1)

    return friendship


async def delete_friendship(
    session: AsyncSession, user_id: int, friend_username: str, cache: AbstractCache | None = None
) -> None:
    friend = await User.get(session, username=friend_username)
    try:
        friendship = await Friendship.get(session, user_id=user_id, friend_id=friend.id)
    except NoResultFound:
        return
    else:
        await friendship.delete(session)
        # Добавляем в кэш новую запись.
        cache_key = f"user_friendships:{user_id}"
        cached_friendship: list[FriendshipEntitySchema] = (await cache.get(cache_key)) or []
        new_friendships = [fs for fs in cached_friendship if fs.id != friend.id]
        await cache.set(cache_key, new_friendships, expire=-1)


async def search_chat_entities(
    session: AsyncSession, search: str, entity_id: int | None = None
) -> list[FriendshipEntitySchema]:
    query = select(User.id, User.username, User.first_name, User.last_name)

    if entity_id is not None:
        query = query.where(User.id == entity_id)
    if len(search) > 3:
        query = query.where(User.username.contains(search))

    result = await session.execute(query)

    return [
        FriendshipEntitySchema(
            id=user[0],
            username=user[1],
            first_name=user[2],
            last_name=user[3],
            type="user",
        )
        for user in result
    ]
