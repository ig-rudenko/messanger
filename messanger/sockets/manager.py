import asyncio
from abc import ABC, abstractmethod
from asyncio import Task
from datetime import datetime
from functools import cache
from logging import getLogger

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from redis.asyncio import Redis, ConnectionPool, RedisError

from .schemas import MessageRequestSchema, MessageResponseSchema
from .status import set_user_online, set_user_offline, is_user_online
from .storages import (
    MessagesStorage,
    NoMessagesStorage,
    DatabaseDirectMessagesStorage,
    RabbitMQMessagesStorage,
)
from ..cache import AbstractCache, get_cache
from ..chats.messages import update_last_message
from ..deco import singleton
from ..friendships.services import get_user_friendships
from ..orm.session_manager import db_manager
from ..settings import settings, MessageStorageType


class BroadcastManager(ABC):

    @abstractmethod
    async def send(self, message: MessageResponseSchema, chat_id: int):
        pass

    @abstractmethod
    async def run_listener(self, websocket: WebSocket, chat_id: int):
        pass

    @abstractmethod
    async def stop_listener(self, chat_id: int):
        pass


class RedisBroadcastManager(BroadcastManager):
    def __init__(self, redis: Redis):
        self.redis = redis
        self._listener_tasks: dict[int, Task] = {}

    async def send(self, message: MessageResponseSchema, chat_id: int):
        try:
            await self.redis.publish(str(chat_id), message.model_dump_json(by_alias=True))
        except RedisError as e:
            print(e)

    async def run_listener(self, websocket: WebSocket, chat_id: int):
        async def async_listener():
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(str(chat_id))
            try:
                while True:
                    msg = await pubsub.get_message(ignore_subscribe_messages=True, timeout=5)
                    if msg is None or msg["type"] != "message" or msg["data"] is None:
                        continue
                    try:
                        await websocket.send_text(msg["data"].decode("utf-8"))
                    except WebSocketDisconnect:
                        return
            finally:
                # Убедимся, что pubsub закрыт корректно
                await pubsub.unsubscribe()
                await pubsub.close()

        self._listener_tasks[chat_id] = asyncio.create_task(async_listener())

    async def stop_listener(self, chat_id: int):
        task = self._listener_tasks.get(chat_id)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass  # Это ожидаемая ошибка при отмене задач


class LocalBroadcastManager(BroadcastManager):
    async def send(self, message: MessageResponseSchema, chat_id: int):
        print(f"{chat_id}: {message}")

    async def run_listener(self, websocket: WebSocket, chat_id: int):
        pass

    async def stop_listener(self, chat_id: int):
        pass


@singleton
class ConnectionManager:
    def __init__(self, broadcast: BroadcastManager, storage: MessagesStorage, cache: AbstractCache):
        self._active_connections: dict[int, list[WebSocket]] = {}
        self._storage = storage
        self._broadcast_manager = broadcast
        self._cache = cache

        asyncio.create_task(self._check_user_online_status())

    async def connect(self, websocket: WebSocket, user_id: int):
        """Подключение пользователя."""
        self._active_connections.setdefault(user_id, []).append(websocket)

        # Подписываемся на обновления сообщений.
        await self._broadcast_manager.run_listener(websocket, user_id)
        await self._set_online(user_id)

    async def disconnect(self, websocket: WebSocket, user_id: int):
        self._active_connections[user_id].remove(websocket)
        await self._broadcast_manager.stop_listener(user_id)

    async def send_message_locally(self, message: MessageResponseSchema, chat_id: int):
        tasks = []
        for connection in self._active_connections.get(chat_id, []):
            tasks.append(self._send_message_to_websocket(connection, message))
        await asyncio.gather(*tasks)  # Параллельно отправляем сообщения

    @staticmethod
    async def _send_message_to_websocket(websocket: WebSocket, message: MessageResponseSchema):
        try:
            await websocket.send_text(message.model_dump_json(by_alias=True))
        except WebSocketDisconnect:
            pass

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
                    created_at=int(datetime.now().timestamp() * 1000),
                )
                # Сначала отправляем.
                await self.broadcast(response, msg.recipient_id)
                # Перезаписываем в кеш.
                await update_last_message(response, self._cache)
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

    async def _check_user_online_status(self):
        while True:
            for user_id, connections in list(self._active_connections.items()):
                if connections:
                    # Пользователь находится в сети.
                    await self._set_online(user_id)

                # Если до этого был онлайн.
                elif await is_user_online(user_id, self._cache):
                    # Пользователь вышел из сети.
                    await self._set_offline(user_id)

            await asyncio.sleep(5)

    async def _set_online(self, user_id: int):
        """Пользователь находится в сети."""
        await set_user_online(user_id, self._cache)
        await self._send_status_to_all_friendships(user_id, "online")

    async def _set_offline(self, user_id: int):
        """Пользователь вышел из сети."""
        await set_user_offline(user_id, self._cache)
        await self._send_status_to_all_friendships(user_id, "offline")

    async def _send_status_to_all_friendships(self, user_id: int, status: str):
        async with db_manager.session() as session:
            friendships = await get_user_friendships(session, user_id, self._cache)
            tasks = []
            for friendship in friendships:
                if friendship.id == user_id:
                    # Пропускаем самого себя.
                    continue

                if await is_user_online(friendship.id, self._cache):
                    message = MessageResponseSchema(
                        type="change_status",
                        status=status,
                        recipient_id=friendship.id,
                        sender_id=user_id,
                        message=f"Пользователь {user_id} {status}.",
                        created_at=int(datetime.now().timestamp() * 1000),
                    )
                    tasks.append(self.broadcast(message, friendship.id))
            await asyncio.gather(*tasks)  # Параллельная отправка статусов


logger = getLogger(__name__)


@cache
def get_redis_broadcast_manager() -> BroadcastManager:
    logger.info("Использование Redis очереди в качестве broadcast")
    pool = ConnectionPool.from_url(
        settings.broadcast_redis_url,
        max_connections=settings.broadcast_redis_max_connections,
    )
    return RedisBroadcastManager(Redis(connection_pool=pool))


@cache
def get_local_broadcast_manager() -> BroadcastManager:
    logger.info("Использование локальной очереди в качестве broadcast")
    return LocalBroadcastManager()


@cache
def get_broadcast_manager() -> BroadcastManager:
    if settings.broadcast_type == "redis":
        return get_redis_broadcast_manager()
    return get_local_broadcast_manager()


@cache
def get_db_message_storage() -> MessagesStorage:
    logger.info("Использование БД в качестве хранилища сообщений")
    return DatabaseDirectMessagesStorage()


@cache
def get_rmq_message_storage() -> MessagesStorage:
    logger.info("Использование RabbitMQ очереди в качестве хранилища сообщений")
    from messanger.rmq import rmq_connector

    return RabbitMQMessagesStorage(rmq_connector)


async def get_message_storage() -> MessagesStorage:
    if settings.message_storage_type == MessageStorageType.DB_DIRECT:
        return get_db_message_storage()

    if settings.message_storage_type == MessageStorageType.RABBITMQ:
        from messanger.rmq import rmq_connector

        await rmq_connector.run_publisher()
        return get_rmq_message_storage()

    logger.warning("Не используется хранилище сообщений!")
    return NoMessagesStorage()


@cache
def create_connection_manager(
    broadcast_manager: BroadcastManager, message_storage: MessagesStorage
) -> ConnectionManager:
    return ConnectionManager(broadcast_manager, message_storage, cache=get_cache())


async def get_connection_manager() -> ConnectionManager:
    broadcast_manager = get_broadcast_manager()
    message_storage = await get_message_storage()
    return create_connection_manager(broadcast_manager, message_storage)
