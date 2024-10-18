from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from messanger.cache import AbstractCache
from messanger.chats.models import Message
from messanger.sockets.schemas import MessageResponseSchema


async def get_last_messages(
    session: AsyncSession, chat_id: int, user_id: int, limit: int = 100
) -> list[MessageResponseSchema]:
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
        .limit(limit)
    )

    # print(query)

    result = await session.execute(query)

    messages = [
        MessageResponseSchema(
            type="message",
            status="stored",
            message=msg.message,
            recipient_id=msg.recipient_id,
            sender_id=msg.sender_id,
            created_at=int(msg.created_at.timestamp()),
        )
        for msg in result.scalars()
    ]

    return list(reversed(messages))


async def get_one_last_message(
    session: AsyncSession, chat_id: int, user_id: int, cache: AbstractCache | None = None
) -> MessageResponseSchema | None:
    cache_key = f"last_message:{chat_id}:{user_id}"
    if cache is not None:
        if data := await cache.get(cache_key):
            return data

    messages = await get_last_messages(session, chat_id, user_id, limit=1)
    if len(messages):
        await cache.set(cache_key, messages[0], -1)
        return messages[0]


async def update_last_message(message: MessageResponseSchema, cache: AbstractCache):
    cache_key = f"last_message:{message.recipient_id}:{message.sender_id}"
    await cache.set(cache_key, message, -1)
    cache_key = f"last_message:{message.sender_id}:{message.recipient_id}"
    await cache.set(cache_key, message, -1)
