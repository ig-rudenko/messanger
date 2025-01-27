from ..settings import settings
from .base import AbstractCache
from .local import InMemoryCache
from .redis import RedisCache


def get_cache() -> AbstractCache:
    """Возвращает кэш в зависимости от настроек приложения"""
    if settings.redis_cache_url:
        return RedisCache(
            url=settings.redis_cache_url,
            max_connections=settings.redis_cache_max_connections,
        )
    else:
        return InMemoryCache()
