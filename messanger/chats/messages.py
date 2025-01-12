from datetime import datetime, UTC

from sqlalchemy import select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from messanger.cache import AbstractCache
from messanger.chats.models import Message
from messanger.sockets.schemas import MessageResponseSchema


async def get_last_messages(
    session: AsyncSession,
    chat_id: int,
    user_id: int,
    limit: int = 100,
    time_from: datetime | None = None,
    time_to: datetime | None = None,
    status: str = "stored",
) -> list[MessageResponseSchema]:
    """
    Возвращает последние сообщения в чате для пользователя.

    :param session: Объект сессии базы данных.
    :param chat_id: Идентификатор чата.
    :param user_id: Идентификатор пользователя.
    :param limit: Количество сообщений.
    :param time_from: Время начала поиска сообщений.
    :param time_to: Время окончания поиска сообщений.
    :param status: Статус сообщения, которые будут возвращены.
    """

    query = (
        select(Message)
        .where(
            or_(
                and_(Message.recipient_id == chat_id, Message.sender_id == user_id),
                and_(Message.recipient_id == user_id, Message.sender_id == chat_id),
            )
        )
        .distinct(Message.id)
        .order_by(Message.created_at.desc())
    )

    if limit:
        query = query.limit(limit)

    if time_from:
        query = query.where(Message.created_at > time_from)

    if time_to:
        query = query.where(Message.created_at <= time_to)

    result = await session.execute(query)

    messages = [
        MessageResponseSchema(
            type="message",
            status=status,
            message=msg.message,
            recipient_id=msg.recipient_id,
            sender_id=msg.sender_id,
            created_at=int(msg.created_at.timestamp() * 1000),
        )
        for msg in result.scalars()
    ]

    return list(reversed(messages))


async def get_one_last_message(
    session: AsyncSession, chat_id: int, user_id: int, cache: AbstractCache | None = None
) -> MessageResponseSchema | None:
    """
    Возвращает последнее сообщение пользователя в чате.
    :param session: Объект сессии базы данных.
    :param chat_id: Идентификатор чата, для которого необходимо получить последнее сообщение.
    :param user_id: Идентификатор пользователя.
    :param cache: Объект кэша.
    """
    cache_key = f"last_message:{chat_id}:{user_id}"
    if data := await cache.get(cache_key):
        return data

    messages = await get_last_messages(session, chat_id, user_id, limit=1)
    if len(messages):
        await cache.set(cache_key, messages[0], -1)
        return messages[0]


async def update_last_message(message: MessageResponseSchema, cache: AbstractCache):
    """
    Обновляет кэш последнего сообщения как для получателя, так и для отправителя.
    """
    cache_key = f"last_message:{message.recipient_id}:{message.sender_id}"
    await cache.set(cache_key, message, -1)
    cache_key = f"last_message:{message.sender_id}:{message.recipient_id}"
    await cache.set(cache_key, message, -1)


async def get_last_read_messages(
    session: AsyncSession, chat_id: int, user_id: int, cache: AbstractCache, limit: int = 100
) -> list[MessageResponseSchema]:
    """
    Возвращает список последних прочитанных сообщений пользователем в чате.

    :param session: Объект сессии базы данных.
    :param chat_id: Идентификатор чата, для которого необходимо получить список последних прочитанных сообщений.
    :param user_id: Идентификатор пользователя.
    :param cache: Объект кэша.
    :param limit: Количество последних прочитанных сообщений.
    """

    cache_key = f"read_messages:{chat_id}:{user_id}"
    if data := await cache.get(cache_key):
        return data

    last_read_message_time = await get_last_read_message_time(chat_id, user_id, cache=cache)
    read_messages = await get_last_messages(
        session, chat_id, user_id, time_to=last_read_message_time, limit=limit
    )
    await cache.set(cache_key, read_messages, -1)
    return read_messages


async def get_unread_messages(
    session: AsyncSession, chat_id: int, user_id: int, cache: AbstractCache
) -> list[MessageResponseSchema]:
    """
    Возвращает список непрочитанных сообщений пользователем в чате.

    :param session: Объект сессии базы данных.
    :param chat_id: Идентификатор чата, для которого необходимо получить список непрочитанных сообщений.
    :param user_id: Идентификатор пользователя.
    :param cache: Объект кэша.
    """

    last_read_message_time = await get_last_read_message_time(chat_id, user_id, cache=cache)
    unread_messages = await get_last_messages(
        session, chat_id, user_id, time_from=last_read_message_time, status="unread"
    )
    return unread_messages


async def get_unread_messages_count(
    session: AsyncSession, chat_id: int, user_id: int, cache: AbstractCache
) -> int:
    """
    Возвращает количество непрочитанных сообщений пользователем в чате.

    :param session: Объект сессии базы данных.
    :param chat_id: Идентификатор чата, для которого необходимо получить количество непрочитанных сообщений.
    :param user_id: Идентификатор пользователя
    :param cache: Объект кэша.
    """
    last_read_message_time = await get_last_read_message_time(chat_id, user_id, cache=cache)

    query = select(func.count(Message.id)).where(
        and_(
            Message.recipient_id == user_id,
            Message.sender_id == chat_id,
            Message.created_at > last_read_message_time,
        )
    )
    return (await session.execute(query)).scalar_one()


async def get_last_read_message_time(chat_id: int, user_id: int, cache: AbstractCache) -> datetime:
    """
    Возвращает время последнего прочитанного сообщения пользователя в чате.
    Для хранения времени используется кэш.

    :param chat_id: Идентификатор чата.
    :param user_id: Идентификатор пользователя.
    :param cache: Объект кэша.
    """
    cache_key = f"last_read_message_time:{chat_id}:{user_id}"
    last_time: datetime | None = await cache.get(cache_key)
    if last_time is None:
        now = datetime.now()
        await cache.set(f"last_read_message_time:{chat_id}:{user_id}", now, -1)
        return now
    return last_time


async def update_last_read_message_time(
    chat_id: int, user_id: int, new_datetime: datetime, cache: AbstractCache
):
    """
    Обновляет время последнего прочитанного сообщения пользователя в чате.
    Для хранения времени используется кэш.

    Также обнуляет кеш для последних прочитанных сообщений.

    :param chat_id: Идентификатор чата.
    :param user_id: Идентификатор пользователя.
    :param new_datetime: Обновляемое время.
    :param cache: Объект кэша.
    """

    last_read_message_time = await get_last_read_message_time(chat_id, user_id, cache=cache)

    if last_read_message_time > new_datetime:
        return

    await cache.set(f"last_read_message_time:{chat_id}:{user_id}", new_datetime, -1)
    await cache.delete(f"read_messages:{chat_id}:{user_id}")
