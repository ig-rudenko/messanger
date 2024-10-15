from fastapi import APIRouter, Depends

from ..auth.models import User
from ..auth.users import get_current_user
from .schemas import SubscriberSchema
from .services import get_subscribers, create_subscriber, delete_subscriber
from ..orm.session_manager import get_session

router = APIRouter(prefix="/subscribers", tags=["subscribers"])


@router.get("", response_model=list[SubscriberSchema])
async def get_my_subscribers_api_view(user: User = Depends(get_current_user), session=Depends(get_session)):
    return get_subscribers(session, user.id)


@router.post("/{username}", response_model=SubscriberSchema)
async def create_subscriber_api_view(
    username: str, user: User = Depends(get_current_user), session=Depends(get_session)
):
    return await create_subscriber(session, user.id, username)


@router.delete("/{username}", status_code=204)
async def delete_subscriber_api_view(
    username: str, user: User = Depends(get_current_user), session=Depends(get_session)
):
    await delete_subscriber(session, user.id, username)
