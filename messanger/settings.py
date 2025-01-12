from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import field_validator, HttpUrl, RedisDsn


class BroadcastType(str, Enum):
    LOCAL = "local"
    REDIS = "redis"


class MessageStorageType(str, Enum):
    NO_STORAGE = "no_storage"
    DB_DIRECT = "db_direct"
    RABBITMQ = "rabbitmq"


class SyncStorage(str, Enum):
    DATABASE = "database"
    ELASTICSEARCH = "elasticsearch"


class _Settings(BaseSettings):

    broadcast_redis_url: str = "redis://localhost:6379/0"
    broadcast_redis_max_connections: int = 10
    broadcast_type: BroadcastType = BroadcastType.LOCAL  # local or redis

    redis_cache_url: str = "redis://localhost:6379/0"
    redis_cache_max_connections: int = 10

    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    message_storage_type: MessageStorageType = MessageStorageType.DB_DIRECT  # "no_storage", "rabbitmq"

    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24 * 7

    # Настройки для синхронизатора сообщений

    sync_storages: str = "database"  # Через запятую несколько: "db", "elasticsearch"
    sync_bulk_size: int = 100
    sync_rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    sync_rabbitmq_max_connections: int = 10
    sync_rabbitmq_exchange: str = "messanger"
    sync_rabbitmq_routing_key: str = "messanger"
    sync_rabbitmq_queue_name: str = "messanger"

    sync_elasticsearch_hosts: str = "http://localhost:9200"

    @field_validator("sync_storages")
    @classmethod
    def validate_sync_storages(cls, value):
        items = value.split(",")
        [SyncStorage(item.strip()) for item in items]
        return value

    @property
    def sync_storages_list(self) -> list[str]:
        return self.sync_storages.split(",")

    @field_validator("sync_elasticsearch_hosts")
    @classmethod
    def validate_sync_es_hosts(cls, value):
        items = value.split(",")
        [HttpUrl(item.strip()) for item in items]
        return value

    @property
    def sync_elasticsearch_hosts_list(self) -> list[str]:
        return self.sync_elasticsearch_hosts.split(",")

    @field_validator("redis_cache_url", "broadcast_redis_url")
    @classmethod
    def validate_redis_url(cls, value):
        RedisDsn(value)
        return value


settings = _Settings()

print("Текущие настройки:")
for key, value in settings.model_dump().items():
    print(f"     {key} = {value}")
