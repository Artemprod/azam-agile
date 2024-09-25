from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.status import Status
from models.task import Task

from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession



class StatusRepository:
    """Класс для работы с сущностью Status, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_status(self, values: dict) -> Status:
        """Создаём новый Status."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Status).values(**values).returning(Status)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_status_by_id(self, status_id: int) -> Optional[Status]:
        """Получаем Status по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Status).filter(Status.id == status_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_status(self, status_id: int, values: dict):
        """Обновляем Status по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Status).where(Status.id == status_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_status(self, status_id: int):
        """Удаляем Status по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Status).where(Status.id == status_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_statuses(self) -> List[Status]:
        """Получаем список всех статусов без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Status)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_status_with_relations(self, status_id: int) -> Optional[Status]:
        """Получаем Status со всеми связями, включая проекты и задачи."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Status)
                .filter(Status.id == status_id)
                .options(
                    selectinload(Status.projects),  # Подгружаем проекты статуса
                    selectinload(Status.tasks)  # Подгружаем задачи статуса
                ))
                result = await session.execute(query)
                return result.scalars().first()