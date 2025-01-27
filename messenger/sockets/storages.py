from abc import ABC, abstractmethod
from datetime import datetime

import aio_pika

from ..orm.session_manager import db_manager
from .schemas import MessageResponseSchema
from ..chats.models import Message
from ..settings import settings


class MessagesStorage(ABC):

    @abstractmethod
    async def process_message(self, message: MessageResponseSchema):
        pass


class NoMessagesStorage(MessagesStorage):
    async def process_message(self, message: MessageResponseSchema):
        pass


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


class RabbitMQMessagesStorage(MessagesStorage):

    def __init__(self, connector):
        self._rmq_connector = connector

    async def process_message(self, message: MessageResponseSchema):
        await self._rmq_connector.publish_message(message.model_dump_json())
