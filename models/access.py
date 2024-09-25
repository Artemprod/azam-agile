from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class AccessLevel(ModelBase):
    __tablename__ = 'access_levels'
    id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле id
    name: Mapped[str]  # Например: "менеджер", "исполнитель"
    users: Mapped[List["User"]] = relationship(back_populates="role")

    # Создаем индекс для поля name
    __table_args__ = (Index('ix_access_levels_name', 'name'), )

class AccessSetting(ModelBase):
    __tablename__ = 'access_settings'
    id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле id
    permission: Mapped[str]  # Например: "создать проект", "удалить задачу"

    # Создаем индекс для поля permission
    __table_args__ = (Index('ix_access_settings_permission', 'permission'), )

class AccessLevelSetting(ModelBase):
    __tablename__ = 'access_settings_levels'
    access_level_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"), primary_key=True, index=True)  # Добавляем индекс
    access_setting_id: Mapped[int] = mapped_column(ForeignKey("access_settings.id"), primary_key=True, index=True)  # Добавляем индекс
    allowed: Mapped[bool]

    # Создаем составной индекс для полей access_level_id и access_setting_id
    __table_args__ = (Index('ix_access_settings_levels_level_setting', 'access_level_id', 'access_setting_id'), )
