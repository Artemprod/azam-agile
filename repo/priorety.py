from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models.priorety import Priority


class PriorityRepository:
    """Класс для работы с сущностью Priority, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_priority(self, values: dict) -> Priority:
        """Создаём новый Priority."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Priority).values(**values).returning(Priority)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_priority_by_id(self, priority_id: int) -> Optional[Priority]:
        """Получаем Priority по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Priority).filter(Priority.id == priority_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_priority(self, priority_id: int, values: dict):
        """Обновляем Priority по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Priority).where(Priority.id == priority_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_priority(self, priority_id: int):
        """Удаляем Priority по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Priority).where(Priority.id == priority_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_priorities(self) -> List[Priority]:
        """Получаем список всех приоритетов без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Priority)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_priority_with_relations(self, priority_id: int) -> Optional[Priority]:
        """Получаем Priority со всеми связями, включая проекты и задачи."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Priority)
                .filter(Priority.id == priority_id)
                .options(
                    selectinload(Priority.projects),  # Подгружаем проекты приоритета
                    selectinload(Priority.tasks)  # Подгружаем задачи приоритета
                ))
                result = await session.execute(query)
                return result.scalars().first()