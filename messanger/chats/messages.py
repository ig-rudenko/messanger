from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from messanger.sockets.schemas import MessageResponseSchema
from messanger.chats.models import Message


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
