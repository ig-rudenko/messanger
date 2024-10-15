from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from .schemas import SubscriberSchema
from .models import Friendship
from ..auth.models import User


async def get_subscribers(session: AsyncSession, user_id: int) -> list[SubscriberSchema]:
    query = (
        select(User.id, User.username, User.first_name, User.last_name)
        .join(Friendship.user_id)
        .where(Friendship.user_id == user_id)
    )

    result = await session.execute(query)
    print(result)

    subscribers = []
    for row in result:
        subscribers.append(SubscriberSchema(id=row[0], username=row[1], first_name=row[2], last_name=row[3]))

    return subscribers


async def create_subscriber(session: AsyncSession, user_id: int, friend_username: str) -> SubscriberSchema:
    friend = await User.get(session, username=friend_username)

    save_point = await session.begin_nested()
    session.add(Friendship(user_id=user_id, friend_id=friend.id))
    try:
        await save_point.commit()
    except IntegrityError:
        await save_point.rollback()

    return SubscriberSchema(
        id=friend.id, username=friend.username, first_name=friend.first_name, last_name=friend.last_name
    )


async def delete_subscriber(session: AsyncSession, user_id: int, friend_username: str) -> None:
    friend = await User.get(session, username=friend_username)
    try:
        friendship = await Friendship.get(session, user_id=user_id, friend_id=friend.id)
    except NoResultFound:
        return
    else:
        await friendship.delete(session)
