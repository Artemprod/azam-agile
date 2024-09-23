from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at



class AccessLevel(ModelBase):
    __tablename__ = 'access_levels'
    id: Mapped[intpk]
    name: Mapped[str]  # Например: "менеджер", "исполнитель"

    users: Mapped[List["User"]] = relationship(back_populates="access_level")


class AccessSetting(ModelBase):
    __tablename__ = 'access_settings'
    id: Mapped[intpk]
    permission: Mapped[str]  # Например: "создать проект", "удалить задачу"
    access_level_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"))
    allowed: Mapped[bool]


class UserAccessLevel(ModelBase):
    __tablename__ = 'user_access_levels'
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    access_level_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"), primary_key=True)
