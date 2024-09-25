from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.report import Report


class ReportRepository:
    """Класс для работы с сущностью Report, включающий методы для получения данных с и без связей"""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_report(self, values: dict) -> Report:
        """Создаём новый Report."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(Report).values(**values).returning(Report)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """Получаем Report по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Report).filter(Report.report_id == report_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_report(self, report_id: int, values: dict):
        """Обновляем Report по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(Report).where(Report.report_id == report_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_report(self, report_id: int):
        """Удаляем Report по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(Report).where(Report.report_id == report_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_reports(self) -> List[Report]:
        """Получаем список всех отчетов без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Report)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_report_with_relations(self, report_id: int) -> Optional[Report]:
        """Получаем Report со всеми связями, включая проект."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(Report).filter(Report.report_id == report_id).options(
                    joinedload(Report.project)  # Подгружаем проект отчёта
                )
                result = await session.execute(query)
                return result.scalars().first()