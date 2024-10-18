from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    broadcast_redis_url: str = "redis://localhost:6379/0"
    broadcast_redis_max_connections: int = 10

    redis_cache_url: str = ""
    redis_cache_max_connections: int = 10
    broadcast_type: str = "local"  # local or redis

    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    message_storage_type: str = "db_direct"

    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24 * 7


settings = _Settings()
