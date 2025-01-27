from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from messenger.chats.models import Message
from messenger.sockets.schemas import MessageResponseSchema
from messenger.orm.session_manager import db_manager


class BaseSynchronizer(ABC):
    """
    Base class for synchronizers.
    """

    @abstractmethod
    async def synchronize(self, messages: list[MessageResponseSchema]):
        """
        Synchronize data.
        """
        pass


class DataBaseSynchronizer(BaseSynchronizer):
    """
    Synchronizer for database.
    """

    async def synchronize(self, messages: list[MessageResponseSchema]):
        async with db_manager.session() as session:  # type: AsyncSession
            stmt = insert(Message).values(
                [
                    {
                        "sender_id": message.sender_id,
                        "recipient_id": message.recipient_id,
                        "message": message.message,
                        "created_at": datetime.fromtimestamp(message.created_at / 1000),
                    }
                    for message in messages
                ]
            )
            await session.execute(stmt)
            await session.commit()


class ElasticsearchSynchronizer(BaseSynchronizer):
    """
    Synchronizer for elasticsearch.
    """

    async def synchronize(self, messages: list[MessageResponseSchema]):
        pass
