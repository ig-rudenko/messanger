from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_scoped_session,
)


class DatabaseSessionManager:
    """
    Менеджер сессий базы данных с поддержкой асинхронности.

    Класс предоставляет методы для инициализации,
    закрытия соединения с базой данных, а также создания
    асинхронных сессий и подключений.
    """

    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, dsn: str, pool_size: int = 10, **conn_args) -> None:
        """Инициализирует соединение с базой данных."""
        if "sqlite" in dsn:
            self._engine = create_async_engine(
                url=dsn,
                connect_args=conn_args,
                # echo=True,
            )
        else:
            self._engine = create_async_engine(
                url=dsn,
                pool_size=pool_size,  # Размер пула соединений
                max_overflow=5,  # Максимальное количество "временных" соединений сверх пула
                pool_timeout=10,  # Тайм-аут ожидания соединения
                pool_pre_ping=True,
                connect_args=conn_args,
                # echo=True,
            )
        self._session_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._session_maker

    async def close(self) -> None:
        """Закрывает соединение с базой данных."""

        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._session_maker = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Контекстный менеджер для создания асинхронной сессии.

        В качестве контекста возвращает объект `AsyncSession`.
        В случае возникновения исключения внутри контекста,
        откатывает транзакцию.
        """
        if self._session_maker is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Контекстный менеджер для создания асинхронного подключения.

        В качестве контекста возвращает объект `AsyncConnection`.
        В случае возникновения исключения внутри контекста,
        откатывает транзакцию.
        """
        if self._engine is None:
            raise IOError("DatabaseSessionManager is not initialized")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager: DatabaseSessionManager = DatabaseSessionManager()


async def get_session() -> AsyncIterator[AsyncSession]:
    """Контекстный менеджер для создания асинхронной сессии."""

    # noinspection PyArgumentList
    async with db_manager.session() as session:
        yield session


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        db_manager.session_maker,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()
