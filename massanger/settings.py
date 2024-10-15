from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 10

    broadcast_type: str = "local"

    database_url: str = "sqlite+aiosqlite:///db.sqlite3"

    access_token_expire_minutes: int = 60
    refresh_token_expire_hours: int = 24 * 7


settings = _Settings()
