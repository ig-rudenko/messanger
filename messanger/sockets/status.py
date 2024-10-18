from messanger.cache import AbstractCache


async def set_user_online(user_id: int, cache: AbstractCache):
    await cache.set(f"{user_id}_online", True, expire=-1)


async def set_user_offline(user_id: int, cache: AbstractCache):
    await cache.set(f"{user_id}_online", False, expire=-1)


async def is_user_online(user_id: int, cache: AbstractCache) -> bool:
    status = await cache.get(f"{user_id}_online")
    return status or False
