from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..orm.session_manager import db_manager
from .schemas import MessageResponseSchema
from ..chats.models import Message


class MessagesStorage(ABC):

    @abstractmethod
    async def process_message(self, message: MessageResponseSchema):
        pass

    @abstractmethod
    async def get_messages(
        self, sender_id: int, recipient_id: int, from_date: datetime, to_date: datetime
    ) -> list[MessageResponseSchema]:
        pass


class NoMessagesStorage(MessagesStorage):
    async def process_message(self, message: MessageResponseSchema):
        pass

    async def get_messages(
        self, sender_id: int, recipient_id: int, from_date: datetime, to_date: datetime
    ) -> list[MessageResponseSchema]:
        return []


class DatabaseDirectMessagesStorage(MessagesStorage):

    async def process_message(self, message: MessageResponseSchema):
        async with db_manager.session() as session:
            session.add(
                Message(
                    message=message.message,
                    sender_id=message.sender_id,
                    recipient_id=message.recipient_id,
                    created_at=datetime.now(),
                )
            )
            await session.commit()

    async def get_messages(
        self, sender_id: int, recipient_id: int, from_date: datetime, to_date: datetime, limit: int = 50
    ) -> list[MessageResponseSchema]:
        async with db_manager.session() as session:  # type: AsyncSession
            query = (
                select(Message)
                .where(
                    Message.sender_id == sender_id,
                    Message.recipient_id == recipient_id,
                    Message.created_at >= from_date,
                    Message.created_at <= to_date,
                )
                .limit(limit)
            )

            result = await session.execute(query)
            return [
                MessageResponseSchema(
                    type="message",
                    status="stored",
                    recipient_id=row.recipient_id,
                    sender_id=row.sender_id,
                    message=row.message,
                    created_at=int(row.created_at.timestamp()),
                )
                for row in result.scalars()
            ]
