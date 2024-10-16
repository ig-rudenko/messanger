from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import WebSocket
from pydantic import ValidationError
from redis.asyncio import Redis, ConnectionPool

from .storages import MessagesStorage, NoMessagesStorage, DatabaseDirectMessagesStorage
from ..settings import settings
from .schemas import MessageRequestSchema, MessageResponseSchema


class BroadcastManager(ABC):

    @abstractmethod
    async def send(self, message: MessageResponseSchema, chat_id: int):
        pass


class RedisBroadcastManager(BroadcastManager):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def send(self, message: MessageResponseSchema, chat_id: int):
        await self.redis.publish(str(chat_id), message.model_dump_json())


class LocalBroadcastManager(BroadcastManager):
    async def send(self, message: MessageResponseSchema, chat_id: int):
        print(f"{chat_id}: {message}")


class ConnectionManager:
    def __init__(self, broadcast: BroadcastManager, storage: MessagesStorage):
        self._active_connections: dict[int, list[WebSocket]] = {}
        self._storage = storage
        self._broadcast_manager = broadcast

    async def connect(self, websocket: WebSocket, user_id: int):
        self._active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        self._active_connections[user_id].remove(websocket)

    async def send_message_locally(self, message: MessageResponseSchema, chat_id: int):
        for connection in self._active_connections.get(chat_id, []):
            await connection.send_text(message.model_dump_json())

    async def analyze_message(self, data: str, sender_user_id: int):
        try:
            msg = MessageRequestSchema.model_validate_json(data)
            if msg.type == "message" and msg.recipient_id:
                response = MessageResponseSchema(
                    type=msg.type,
                    status=msg.status,
                    message=msg.message.strip(),
                    recipient_id=msg.recipient_id,
                    sender_id=sender_user_id,
                    created_at=int(datetime.now().timestamp()),
                )
                # Сначала отправляем.
                await self.broadcast(response, msg.recipient_id)
                # Затем обрабатываем сохранение.
                await self._storage.process_message(response)

        except ValidationError as e:
            print(e)

    async def broadcast(self, message: MessageResponseSchema, chat_id: int):
        if self._active_connections.get(chat_id, []):
            # Оба пользователя на одном сервере, передаем сообщение напрямую
            await self.send_message_locally(message, chat_id)
        else:
            # Пользователи на разных серверах, используем Redis для передачи
            await self._broadcast_manager.send(message, chat_id)


def get_broadcast_manager() -> BroadcastManager:
    if settings.broadcast_type == "redis":
        pool = ConnectionPool.from_url(settings.redis_url, max_connections=settings.redis_max_connections)
        return RedisBroadcastManager(Redis(connection_pool=pool))

    return LocalBroadcastManager()


def get_storage() -> MessagesStorage:
    if settings.message_storage_type == "db_direct":
        return DatabaseDirectMessagesStorage()
    return NoMessagesStorage()


message_storage = get_storage()
broadcast_manager = get_broadcast_manager()
manager = ConnectionManager(broadcast_manager, message_storage)
