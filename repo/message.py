from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.message import Message


class MessageRepository:
    """Класс для работы с сущностью Message, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_message(self, values: dict) -> Message:
        """Создаём новое Message."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Message).values(**values).returning(Message)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """Получаем Message по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Message).filter(Message.message_id == message_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_message(self, message_id: int, values: dict):
        """Обновляем Message по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Message).where(Message.message_id == message_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_message(self, message_id: int):
        """Удаляем Message по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Message).where(Message.message_id == message_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_messages(self) -> List[Message]:
        """Получаем список всех сообщений без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Message)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_message_with_relations(self, message_id: int) -> Optional[Message]:
        """Получаем Message со всеми связями, включая пользователя и чат."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Message)
                .filter(Message.message_id == message_id)
                .options(
                    joinedload(Message.user),  # Подгружаем пользователя сообщения
                    joinedload(Message.chat)  # Подгружаем чат сообщения
                ))
                result = await session.execute(query)
                return result.scalars().first()