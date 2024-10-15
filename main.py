from contextlib import asynccontextmanager

from fastapi import FastAPI

from massanger.orm.session_manager import db_manager
from massanger.settings import settings
from massanger.sockets.handlers import router as sockets_router
from massanger.auth.handlers import router as auth_router
from massanger.subscribers.handlers import router as subscribers_router


@asynccontextmanager
async def startup(app_instance: FastAPI):
    db_manager.init(settings.database_url)
    yield
    await db_manager.close()


app = FastAPI(lifespan=startup)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(subscribers_router, prefix="/api/v1")
app.include_router(sockets_router, prefix="/ws")


@app.get("/ping")
def health():
    return "pong"
