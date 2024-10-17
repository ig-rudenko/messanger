from fastapi import Depends, APIRouter

from messanger.auth.models import User
from messanger.auth.users import get_current_user
from messanger.chats.messages import get_last_messages
from messanger.orm.session_manager import get_session
from messanger.sockets.schemas import MessageResponseSchema


router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/{chat_id}/lastMessages", response_model=list[MessageResponseSchema])
async def get_last_messages_api_view(
    chat_id: int,
    user: User = Depends(get_current_user),
    session=Depends(get_session),
):
    return await get_last_messages(session, chat_id, user.id)
