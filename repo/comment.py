from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.comment import Comment


class CommentRepository:
    """Класс для работы с сущностью Comment, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_comment(self, values: dict) -> Comment:
        """Создаём новый Comment."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Comment).values(**values).returning(Comment)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        """Получаем Comment по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Comment).filter(Comment.comment_id == comment_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_comment(self, comment_id: int, values: dict):
        """Обновляем Comment по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Comment).where(Comment.comment_id == comment_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_comment(self, comment_id: int):
        """Удаляем Comment по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Comment).where(Comment.comment_id == comment_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_comments(self) -> List[Comment]:
        """Получаем список всех комментариев без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Comment)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_comment_with_relations(self, comment_id: int) -> Optional[Comment]:
        """Получаем Comment со всеми связями, включая пользователя, проект и задачу."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Comment)
                .filter(Comment.comment_id == comment_id)
                .options(
                    joinedload(Comment.user),  # Подгружаем пользователя комментария
                    joinedload(Comment.project),  # Подгружаем проект комментария
                    joinedload(Comment.task)  # Подгружаем задачу комментария
                ))
                result = await session.execute(query)
                return result.scalars().first()
