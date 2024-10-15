from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .auth import authenticate_websocket
from .manager import manager
from ..auth.models import User

router = APIRouter(prefix="", tags=["ws"])


# WebSocket для личной переписки
@router.websocket("")
async def private_chat(websocket: WebSocket, user: User = Depends(authenticate_websocket)):
    await manager.connect(websocket, user.username)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.analyze_message(data, user.username)
            # await manager.broadcast(f"{user.id}: {data}", user.id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.username)


# eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTkwNzUyfQ.gxb-C0wOM7U941Zvo54c2lGZSiTLLAdqCvTrH2slqg3UBHzNE6oQEzA_SWzd4VgRqW6j35E47n0gKrLfNrAtqw
# {"type": "message", "status": "ok", "message": "Hello World!", "recipientUsername": "user2"}

# eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTkxNzQ3fQ.DHkzvzJs8CKB_AYDqFTvsT1efMJcfyoqeZ1Hr-q0JZ1qv7bhrzL1J6mb_386gA-LgOwJYw2IGF0jLV5_106tqQ
# {"type": "message", "status": "ok", "message": "Hi!", "recipientUsername": "user1"}

# # WebSocket для общения в группе
# @router.websocket("/group/{group_id}")
# async def group_chat(websocket: WebSocket, group_id: str):
#     await manager.connect(websocket, group_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(data, group_id)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket, group_id)
