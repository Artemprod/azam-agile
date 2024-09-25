from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.notification import Notification


class NotificationRepository:
    """Класс для работы с сущностью Notification, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_notification(self, values: dict) -> Notification:
        """Создаём новую Notification."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Notification).values(**values).returning(Notification)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Получаем Notification по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Notification).filter(Notification.id == notification_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_notification(self, notification_id: int, values: dict):
        """Обновляем Notification по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Notification).where(Notification.id == notification_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_notification(self, notification_id: int):
        """Удаляем Notification по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Notification).where(Notification.id == notification_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_notifications(self) -> List[Notification]:
        """Получаем список всех уведомлений без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Notification)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_notification_with_relations(self, notification_id: int) -> Optional[Notification]:
        """Получаем Notification со всеми связями, включая пользователя."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(Notification)
                .filter(Notification.id == notification_id)
                .options(
                    joinedload(Notification.user)  # Подгружаем пользователя уведомления
                ))
                result = await session.execute(query)
                return result.scalars().first()