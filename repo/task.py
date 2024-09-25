from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Task


class TaskRepository:
    """Класс для работы с сущностью Task, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_task(self, values: dict) -> Task:
        """Создаём новый Task."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Task).values(**values).returning(Task)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Получаем Task по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Task).filter(Task.task_id == task_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_task(self, task_id: int, values: dict):
        """Обновляем Task по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Task).where(Task.task_id == task_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_task(self, task_id: int):
        """Удаляем Task по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Task).where(Task.task_id == task_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_tasks(self) -> List[Task]:
        """Получаем список всех задач без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Task)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_task_with_relations(self, task_id: int) -> Optional[Task]:
        """Получаем Task со всеми связями."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Task)
                .filter(Task.task_id == task_id)
                .options(
                    joinedload(Task.priority),  # Подгружаем приоритет задачи
                    joinedload(Task.status),  # Подгружаем статус задачи
                    joinedload(Task.executor),  # Подгружаем исполнителя задачи
                    joinedload(Task.project),  # Подгружаем проект задачи
                    joinedload(Task.chat),  # Подгружаем чат задачи
                    selectinload(Task.assigned_users)  # Подгружаем назначенных пользователей
                ))
                result = await session.execute(query)
                return result.scalars().first()