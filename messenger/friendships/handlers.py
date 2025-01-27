from fastapi import APIRouter, Depends, Query

from .schemas import FriendshipEntitySchema, NewFriendshipEntitySchema, ExistingFriendshipEntitySchema
from .services import create_friendship, delete_friendship, search_chat_entities, get_my_friendships_data
from ..auth.models import User
from ..auth.users import get_current_user
from ..cache import AbstractCache, get_cache
from ..orm.session_manager import get_session

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.get("", response_model=list[ExistingFriendshipEntitySchema])
async def get_my_friendships_api_view(
    user: User = Depends(get_current_user),
    session=Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
):
    return await get_my_friendships_data(session, user.id, cache=cache)


@router.post("", response_model=FriendshipEntitySchema)
async def create_friendship_api_view(
    data: NewFriendshipEntitySchema,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
):
    return await create_friendship(session, user.id, data.username, cache=cache)


@router.delete("/{username}", status_code=204)
async def delete_friendship_api_view(
    username: str,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
    cache: AbstractCache = Depends(get_cache),
):
    await delete_friendship(session, user.id, username, cache=cache)


@router.get("/search", response_model=list[FriendshipEntitySchema])
async def search_chat_entities_api_view(
    search: str = Query("", max_length=100),
    entity_id: int | None = Query(None),
    _=Depends(get_current_user),
    session=Depends(get_session),
):
    return await search_chat_entities(session, search, entity_id)
