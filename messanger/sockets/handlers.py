from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .auth import authenticate_websocket
from .manager import manager
from ..auth.models import User

router = APIRouter(prefix="", tags=["ws"])


@router.websocket("")
async def private_chat(websocket: WebSocket, user: User = Depends(authenticate_websocket)):
    """WebSocket для личной переписки"""
    await manager.connect(websocket, user.id)

    try:
        while True:
            data = await websocket.receive_text()  # Ожидание сообщения от сокета.
            await manager.analyze_message(data, user.id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user.id)
