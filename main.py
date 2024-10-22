from contextlib import asynccontextmanager

from fastapi import FastAPI

from messanger.auth.handlers import router as auth_router
from messanger.chats.handlers import router as chats_router
from messanger.friendships.handlers import router as friendships_router
from messanger.orm.session_manager import db_manager
from messanger.settings import settings
from messanger.sockets.handlers import router as sockets_router


@asynccontextmanager
async def startup(app_instance: FastAPI):
    db_manager.init(settings.database_url)
    yield
    await db_manager.close()


app = FastAPI(lifespan=startup)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(friendships_router, prefix="/api/v1")
app.include_router(chats_router, prefix="/api/v1")
app.include_router(sockets_router, prefix="/ws")


@app.get("/ping", tags=["health"])
def health():
    return "pong"
