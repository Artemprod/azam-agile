from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at





class Status(ModelBase):
    __tablename__ = 'statuses'
    id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле id
    name: Mapped[str]  # Индексируем поле name
    type: Mapped[str]  # Индексируем поле type ("project" или "task")

    # Проекты, которым назначен статус
    projects: Mapped[list["Project"]] = relationship(back_populates="status")
    # Задачи, которым назначен статус
    tasks: Mapped[list["Task"]] = relationship(back_populates="status")

    # Создаем индексы для полей name и type
    __table_args__ = (
        Index('ix_statuses_name', 'name'),
        Index('ix_statuses_type', 'type'),
    )