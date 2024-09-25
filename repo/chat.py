from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models.chat import Chat


class ChatRepository:
    """Класс для работы с сущностью Chat, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_chat(self, values: dict) -> Chat:
        """Создаём новый Chat."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Chat).values(**values).returning(Chat)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        """Получаем Chat по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Chat).filter(Chat.chat_id == chat_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_chat(self, chat_id: int, values: dict):
        """Обновляем Chat по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Chat).where(Chat.chat_id == chat_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_chat(self, chat_id: int):
        """Удаляем Chat по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Chat).where(Chat.chat_id == chat_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_chats(self) -> List[Chat]:
        """Получаем список всех чатов без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Chat)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_chat_with_relations(self, chat_id: int) -> Optional[Chat]:
        """Получаем Chat со всеми связями, включая проект, задачу и сообщения."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Chat)
                .filter(Chat.chat_id == chat_id)
                .options(
                    joinedload(Chat.project),  # Подгружаем проект чата
                    joinedload(Chat.task),  # Подгружаем задачу чата
                    selectinload(Chat.messages)  # Подгружаем сообщения чата
                ))
                result = await session.execute(query)
                return result.scalars().first()