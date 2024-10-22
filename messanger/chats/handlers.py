from datetime import datetime

from fastapi import Depends, APIRouter

from messanger.auth.models import User
from messanger.auth.users import get_current_user
from messanger.cache import get_cache
from messanger.chats.messages import (
    update_last_read_message_time,
    get_last_read_message_time,
    get_unread_messages_count,
    get_last_messages,
)
from messanger.chats.schemas import UpdateLastReadSchema, LastReadSchema
from messanger.orm.session_manager import get_session
from messanger.sockets.schemas import MessageResponseSchema

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/{chat_id}/lastMessages", response_model=list[MessageResponseSchema])
async def get_last_messages_api_view(
    chat_id: int,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    unread_messages_count = await get_unread_messages_count(session, chat_id, user.id, cache=get_cache())
    return await get_last_messages(session, chat_id, user.id, limit=100 + unread_messages_count)


@router.get("/{chat_id}/unreadMessagesCount", response_model=int)
async def get_unread_messages_count_api_view(
    chat_id: int,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    return await get_unread_messages_count(session, chat_id, user.id, cache=get_cache())


@router.get("/{chat_id}/lastRead", status_code=200, response_model=LastReadSchema)
async def get_last_read_api_view(
    chat_id: int,
    user: User = Depends(get_current_user),
):
    last_read_message_time = await get_last_read_message_time(chat_id, user.id, cache=get_cache())
    timestamp = int(last_read_message_time.timestamp())
    return LastReadSchema(timestamp=timestamp)


@router.post("/{chat_id}/lastRead", status_code=200)
async def update_last_read_api_view(
    data: UpdateLastReadSchema,
    chat_id: int,
    user: User = Depends(get_current_user),
):
    await update_last_read_message_time(
        chat_id, user.id, new_datetime=datetime.fromtimestamp(data.timestamp + 1), cache=get_cache()
    )
