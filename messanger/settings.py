import logging
from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import field_validator, HttpUrl, RedisDsn


class SyncStorage(str, Enum):
    DATABASE = "database"
    ELASTICSEARCH = "elasticsearch"


class _SyncSettings(BaseSettings):
    """
    Настройки для синхронизатора сообщений
    """

    storages: str = "database"  # Через запятую несколько: "db", "elasticsearch"
    bulk_size: int = 100
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_max_connections: int = 10
    rabbitmq_exchange: str = "messanger"
    rabbitmq_routing_key: str = "messanger"
    rabbitmq_queue_name: str = "messanger"

    elasticsearch_hosts: str = "http://localhost:9200"

    @field_validator("storages")
    @classmethod
    def validate_storages(cls, value):
        items = value.split(",")
        [SyncStorage(item.strip()) for item in items]
        return value

    @property
    def storages_list(self) -> list[str]:
        return self.storages.split(",")

    @field_validator("elasticsearch_hosts")
    @classmethod
    def validate_es_hosts(cls, value):
        items = value.split(",")
        [HttpUrl(item.strip()) for item in items]
        return value

    @property
    def elasticsearch_hosts_list(self) -> list[str]:
        return self.elasticsearch_hosts.split(",")


class BroadcastType(str, Enum):
    LOCAL = "local"
    REDIS = "redis"


class MessageStorageType(str, Enum):
    NO_STORAGE = "no_storage"
    DB_DIRECT = "db_direct"
    RABBITMQ = "rabbitmq"


class _Settings(BaseSettings):
    log_level: str = "INFO"

    broadcast_type: BroadcastType = BroadcastType.LOCAL  # local or redis
    broadcast_redis_url: str = "redis://localhost:6379/0"
    broadcast_redis_max_connections: int = 10

    redis_cache_url: str = "redis://localhost:6379/0"
    redis_cache_max_connections: int = 10

    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    database_max_connections: int = 10

    message_storage_type: MessageStorageType = MessageStorageType.DB_DIRECT  # "no_storage", "rabbitmq"

    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24 * 7

    sync: _SyncSettings = _SyncSettings(_env_prefix="sync_")

    @field_validator("redis_cache_url", "broadcast_redis_url")
    @classmethod
    def validate_redis_url(cls, value):
        if value:
            RedisDsn(value)
        return value


settings = _Settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

logger.info("Текущие настройки:")
for key, val in settings.model_dump().items():
    logger.info(f"{key} = {val}")
