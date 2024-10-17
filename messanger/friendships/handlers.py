from fastapi import APIRouter, Depends, Query

from ..auth.models import User
from ..auth.users import get_current_user
from .schemas import FriendshipEntitySchema, NewFriendshipEntitySchema, ExistingFriendshipEntitySchema
from .services import get_user_friendships, create_friendship, delete_friendship, search_chat_entities
from ..orm.session_manager import get_session

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.get("", response_model=list[ExistingFriendshipEntitySchema])
async def get_my_friendships_api_view(
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    return await get_user_friendships(session, user.id)


@router.post("", response_model=FriendshipEntitySchema)
async def create_friendship_api_view(
    data: NewFriendshipEntitySchema,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    return await create_friendship(session, user.id, data.username)


@router.delete("/{username}", status_code=204)
async def delete_friendship_api_view(
    username: str,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    await delete_friendship(session, user.id, username)


@router.get("/search", response_model=list[FriendshipEntitySchema])
async def search_chat_entities_api_view(
    search: str = Query(..., min_length=3, max_length=100),
    _=Depends(get_current_user),
    session=Depends(get_session),
):
    return await search_chat_entities(session, search)
