from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


class UserRepository:
    """Класс для работы с сущностью User, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_user(self, values: dict) -> User:
        """Создаём нового User."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(User).values(**values).returning(User)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получаем User по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(User).filter(User.user_id == user_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_user(self, user_id: int, values: dict):
        """Обновляем User по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(User).where(User.user_id == user_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_user(self, user_id: int):
        """Удаляем User по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(User).where(User.user_id == user_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_users(self) -> List[User]:
        """Получаем список всех пользователей без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_user_with_relations(self, user_id: int) -> Optional[User]:
        """Получаем User со всеми связями."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(User)
                .filter(User.user_id == user_id)
                .options(
                    joinedload(User.role),  # Подгружаем роль пользователя
                    joinedload(User.projects_owned),  # Подгружаем проекты пользователя
                    joinedload(User.notifications),  # Подгружаем уведомления пользователя
                    joinedload(User.messages),  # Подгружаем сообщения пользователя
                    selectinload(User.project_assigned),  # Подгружаем проекты, на которые пользователь назначен
                    selectinload(User.tasks_assigned)  # Подгружаем задачи, на которые пользователь назначен
                ))
                result = await session.execute(query)
                return result.scalars().first()
