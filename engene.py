from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class DatabaseSessionManager:
    def __init__(self, database_url: str):
        # Настройка асинхронного движка SQLAlchemy с параметрами пула соединений
        self.engine = create_async_engine(
            database_url,
            echo=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
        )

        # Создание фабрики для асинхронных сессий
        self.async_session_factory = async_sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)

