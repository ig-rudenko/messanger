from contextlib import asynccontextmanager

from fastapi import FastAPI

from messenger.auth.handlers import router as auth_router
from messenger.chats.handlers import router as chats_router
from messenger.friendships.handlers import router as friendships_router
from messenger.orm.session_manager import db_manager
from messenger.settings import settings
from messenger.sockets.handlers import router as sockets_router


@asynccontextmanager
async def startup(app_instance: FastAPI):
    db_manager.init(settings.database_url, pool_size=settings.database_max_connections)
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
