from fastapi import WebSocket, Depends, HTTPException

from messenger.auth.models import User
from messenger.auth.users import get_current_user
from messenger.orm.session_manager import get_session


async def authenticate_websocket(websocket: WebSocket, session=Depends(get_session)) -> User:
    await websocket.accept()
    # Получаем токен из тела сообщения
    token = await websocket.receive_text()
    # Получаем пользователя
    try:
        user: User = await get_current_user(token, session)
    except HTTPException as exc:
        await websocket.send_json({"type": "system", "status": "exception", "message": exc.detail})
        await websocket.close()
        raise exc
    else:
        await websocket.send_json({"type": "system", "status": "ok", "message": "Connected"})

    return user
