from sqlalchemy import select, insert, update, delete
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.assigned import ProjectAssigned, TaskAssigned


class ProjectAssignedRepository:
    """Класс для работы с сущностью ProjectAssigned."""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_project_assigned(self, values: dict) -> ProjectAssigned:
        """Создаём новую запись ProjectAssigned."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(ProjectAssigned).values(**values).returning(ProjectAssigned)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_project_assigned_by_id(self, user_id: int, project_id: int) -> Optional[ProjectAssigned]:
        """Получаем ProjectAssigned по составному ключу user_id и project_id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(ProjectAssigned).filter(
                    ProjectAssigned.user_id == user_id,
                    ProjectAssigned.project_id == project_id
                )
                result = await session.execute(query)
                return result.scalars().first()

    async def update_project_assigned(self, user_id: int, project_id: int, values: dict):
        """Обновляем ProjectAssigned по составному ключу user_id и project_id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(ProjectAssigned).where(
                    ProjectAssigned.user_id == user_id,
                    ProjectAssigned.project_id == project_id
                ).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_project_assigned(self, user_id: int, project_id: int):
        """Удаляем ProjectAssigned по составному ключу user_id и project_id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(ProjectAssigned).where(
                    ProjectAssigned.user_id == user_id,
                    ProjectAssigned.project_id == project_id
                )
                await session.execute(stmt)
                await session.commit()

    async def get_all_project_assigned(self) -> List[ProjectAssigned]:
        """Получаем список всех записей ProjectAssigned без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(ProjectAssigned)
                result = await session.execute(query)
                return result.scalars().all()


class TaskAssignedRepository:
    """Класс для работы с сущностью TaskAssigned."""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_task_assigned(self, values: dict) -> TaskAssigned:
        """Создаём новую запись TaskAssigned."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(TaskAssigned).values(**values).returning(TaskAssigned)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_task_assigned_by_id(self, user_id: int, task_id: int) -> Optional[TaskAssigned]:
        """Получаем TaskAssigned по составному ключу user_id и task_id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(TaskAssigned).filter(
                    TaskAssigned.user_id == user_id,
                    TaskAssigned.task_id == task_id
                )
                result = await session.execute(query)
                return result.scalars().first()

    async def update_task_assigned(self, user_id: int, task_id: int, values: dict):
        """Обновляем TaskAssigned по составному ключу user_id и task_id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(TaskAssigned).where(
                    TaskAssigned.user_id == user_id,
                    TaskAssigned.task_id == task_id
                ).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_task_assigned(self, user_id: int, task_id: int):
        """Удаляем TaskAssigned по составному ключу user_id и task_id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(TaskAssigned).where(
                    TaskAssigned.user_id == user_id,
                    TaskAssigned.task_id == task_id
                )
                await session.execute(stmt)
                await session.commit()

    async def get_all_task_assigned(self) -> List[TaskAssigned]:
        """Получаем список всех записей TaskAssigned без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(TaskAssigned)
                result = await session.execute(query)
                return result.scalars().all()
