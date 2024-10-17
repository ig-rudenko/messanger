from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from .schemas import FriendshipEntitySchema, ExistingFriendshipEntitySchema
from .models import Friendship
from ..chats.messages import get_last_messages
from ..auth.models import User


async def get_user_friendships(session: AsyncSession, user_id: int) -> list[ExistingFriendshipEntitySchema]:
    query = (
        select(User.id, User.username, User.first_name, User.last_name)
        .join(Friendship, Friendship.friend_id == User.id)
        .where(Friendship.user_id == user_id)
    )

    result = await session.execute(query)

    friendships = []
    for row in result:
        friendship_id = row[0]
        last_message = await get_last_messages(session, chat_id=friendship_id, user_id=user_id, limit=1)
        friendships.append(
            ExistingFriendshipEntitySchema(
                id=friendship_id,
                type="user",
                username=row[1],
                first_name=row[2],
                last_name=row[3],
                last_message=last_message[0].message if last_message else None,
                last_datetime=last_message[0].created_at if last_message else None,
            )
        )

    return friendships


async def create_friendship(
    session: AsyncSession, user_id: int, friend_username: str
) -> FriendshipEntitySchema:
    friend = await User.get(session, username=friend_username)

    save_point = await session.begin_nested()
    session.add(Friendship(user_id=user_id, friend_id=friend.id))
    try:
        await save_point.commit()
    except IntegrityError:
        await save_point.rollback()

    return FriendshipEntitySchema(
        id=friend.id,
        username=friend.username,
        first_name=friend.first_name,
        last_name=friend.last_name,
        type="user",
    )


async def delete_friendship(session: AsyncSession, user_id: int, friend_username: str) -> None:
    friend = await User.get(session, username=friend_username)
    try:
        friendship = await Friendship.get(session, user_id=user_id, friend_id=friend.id)
    except NoResultFound:
        return
    else:
        await friendship.delete(session)


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
