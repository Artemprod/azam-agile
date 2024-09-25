from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.project import Project


class ProjectRepository:
    """Класс для работы с сущностью Project, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_project(self, values: dict) -> Project:
        """Создаём новый Project."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Project).values(**values).returning(Project)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Получаем Project по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Project).filter(Project.project_id == project_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_project(self, project_id: int, values: dict):
        """Обновляем Project по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Project).where(Project.project_id == project_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_project(self, project_id: int):
        """Удаляем Project по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Project).where(Project.project_id == project_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_projects(self) -> List[Project]:
        """Получаем список всех проектов без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Project)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_project_with_relations(self, project_id: int) -> Optional[Project]:
        """Получаем Project со всеми связями."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Project)
                .filter(Project.project_id == project_id)
                .options(
                    joinedload(Project.status),  # Подгружаем статус проекта
                    joinedload(Project.owner),  # Подгружаем владельца проекта
                    joinedload(Project.priority),  # Подгружаем приоритет проекта
                    selectinload(Project.tasks),  # Подгружаем задачи проекта
                    selectinload(Project.reports),  # Подгружаем отчёты проекта
                    joinedload(Project.chat),  # Подгружаем чат проекта
                    selectinload(Project.assigned_users)  # Подгружаем назначенных пользователей
                ))
                result = await session.execute(query)
                return result.scalars().first()