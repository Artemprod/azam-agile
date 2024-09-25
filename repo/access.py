from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import joinedload, selectinload
from typing import List, Optional

from models.access import AccessLevel, AccessSetting, AccessLevelSetting


class AccessLevelRepository:
    """Класс для работы с сущностью AccessLevel."""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_access_level(self, values: dict) -> AccessLevel:
        """Создаём новый AccessLevel."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(AccessLevel).values(**values).returning(AccessLevel)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_access_level_by_id(self, access_level_id: int) -> Optional[AccessLevel]:
        """Получаем AccessLevel по id без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(AccessLevel).filter(AccessLevel.id == access_level_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_access_level(self, access_level_id: int, values: dict):
        """Обновляем AccessLevel по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(AccessLevel).where(AccessLevel.id == access_level_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_access_level(self, access_level_id: int):
        """Удаляем AccessLevel по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(AccessLevel).where(AccessLevel.id == access_level_id)
                await session.execute(stmt)
                await session.commit()

    async def get_all_access_levels(self) -> List[AccessLevel]:
        """Получаем список всех AccessLevel без связанных данных."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(AccessLevel)
                result = await session.execute(query)
                return result.scalars().all()

    async def get_access_level_with_relations(self, access_level_id: int) -> Optional[AccessLevel]:
        """Получаем AccessLevel со всеми связями (например, пользователи)."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = (select(AccessLevel)
                         .filter(AccessLevel.id == access_level_id)
                         .options(joinedload(AccessLevel.users)))
                result = await session.execute(query)
                return result.scalars().first()


class AccessSettingRepository:
    """Класс для работы с сущностью AccessSetting."""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_access_setting(self, values: dict) -> AccessSetting:
        """Создаём новый AccessSetting."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(AccessSetting).values(**values).returning(AccessSetting)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_access_setting_by_id(self, access_setting_id: int) -> Optional[AccessSetting]:
        """Получаем AccessSetting по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(AccessSetting).filter(AccessSetting.id == access_setting_id)
                result = await session.execute(query)
                return result.scalars().first()

    async def update_access_setting(self, access_setting_id: int, values: dict):
        """Обновляем AccessSetting по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(AccessSetting).where(AccessSetting.id == access_setting_id).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_access_setting(self, access_setting_id: int):
        """Удаляем AccessSetting по id."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(AccessSetting).where(AccessSetting.id == access_setting_id)
                await session.execute(stmt)
                await session.commit()

    # Это метод в AccessSettingRepository не имеет логического смысла, так как AccessSetting
    # не имеет прямой связи с AccessLevel. Однако оставим его с комментариями, которые поясняют это.
    async def get_access_settings_for_access_level(self, access_level_id: int) -> List[AccessSetting]:
        """Этот метод не реализован, так как AccessSetting не имеет связи с AccessLevel напрямую."""
        raise NotImplementedError("This method is not applicable for AccessSetting.")


class AccessLevelSettingRepository:
    """Класс для работы с сущностью AccessLevelSetting."""

    def __init__(self, async_session_factory):
        self.async_session_factory = async_session_factory

    async def create_access_level_setting(self, values: dict) -> AccessLevelSetting:
        """Создаём новый AccessLevelSetting."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = insert(AccessLevelSetting).values(**values).returning(AccessLevelSetting)
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()

    async def get_access_level_setting_by_id(self, access_level_id: int, access_setting_id: int) -> Optional[
        AccessLevelSetting]:
        """Получаем AccessLevelSetting по составному ключу."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(AccessLevelSetting).filter(
                    AccessLevelSetting.access_level_id == access_level_id,
                    AccessLevelSetting.access_setting_id == access_setting_id
                )
                result = await session.execute(query)
                return result.scalars().first()

    async def update_access_level_setting(self, access_level_id: int, access_setting_id: int, values: dict):
        """Обновляем AccessLevelSetting по составному ключу."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = update(AccessLevelSetting).where(
                    AccessLevelSetting.access_level_id == access_level_id,
                    AccessLevelSetting.access_setting_id == access_setting_id
                ).values(**values)
                await session.execute(stmt)
                await session.commit()

    async def delete_access_level_setting(self, access_level_id: int, access_setting_id: int):
        """Удаляем AccessLevelSetting по составному ключу."""
        async with self.async_session_factory() as session:
            async with session.begin():
                stmt = delete(AccessLevelSetting).where(
                    AccessLevelSetting.access_level_id == access_level_id,
                    AccessLevelSetting.access_setting_id == access_setting_id
                )
                await session.execute(stmt)
                await session.commit()

    async def get_all_access_level_settings(self) -> List[AccessLevelSetting]:
        """Получаем список всех AccessLevelSetting."""
        async with self.async_session_factory() as session:
            async with session.begin():
                query = select(AccessLevelSetting)
                result = await session.execute(query)
                return result.scalars().all()