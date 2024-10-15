from abc import ABC, abstractmethod

from fastapi import WebSocket
from pydantic import ValidationError
from redis.asyncio import Redis, ConnectionPool

from ..settings import settings
from .schemas import MessageRequestSchema, MessageResponseSchema


class BroadcastManager(ABC):

    @abstractmethod
    async def send(self, message: MessageResponseSchema, chat_id: str):
        pass


class RedisBroadcastManager(BroadcastManager):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def send(self, message: MessageResponseSchema, chat_id: str):
        await self.redis.publish(chat_id, message.model_dump_json())


class LocalBroadcastManager(BroadcastManager):
    async def send(self, message: MessageResponseSchema, chat_id: str):
        print(f"{chat_id}: {message}")


class ConnectionManager:
    def __init__(self, broadcast_manager: BroadcastManager):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.broadcast_manager = broadcast_manager

    async def connect(self, websocket: WebSocket, user_id: str):
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id].remove(websocket)

    async def send_message_locally(self, message: MessageResponseSchema, chat_id: str):
        for connection in self.active_connections.get(chat_id, []):
            await connection.send_text(message.model_dump_json())

    async def analyze_message(self, data: str, sender_username: str):
        try:
            msg = MessageRequestSchema.model_validate_json(data)
            if msg.type == "message" and msg.recipient_username:
                response = MessageResponseSchema(
                    type=msg.type,
                    status=msg.status,
                    message=msg.message,
                    recipient_username=msg.recipient_username,
                    sender_username=sender_username,
                )

                await self.broadcast(response, msg.recipient_username)

        except ValidationError as e:
            print(e)

    async def broadcast(self, message: MessageResponseSchema, chat_id: str):
        if self.active_connections.get(chat_id, []):
            # Оба пользователя на одном сервере, передаем сообщение напрямую
            await self.send_message_locally(message, chat_id)
        else:
            # Пользователи на разных серверах, используем Redis для передачи
            await self.broadcast_manager.send(message, chat_id)


def get_broadcast_manager() -> BroadcastManager:
    if settings.broadcast_type == "redis":
        pool = ConnectionPool.from_url(settings.redis_url, max_connections=settings.redis_max_connections)
        return RedisBroadcastManager(Redis(connection_pool=pool))

    return LocalBroadcastManager()


manager = ConnectionManager(get_broadcast_manager())
