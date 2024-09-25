from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class Priority(ModelBase):
    __tablename__ = 'priorities'
    id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле id
    name: Mapped[str]  # Индексируем поле name
    projects: Mapped[List["Project"]] = relationship(back_populates="priority")
    tasks: Mapped[List["Task"]] = relationship(back_populates="priority")

    # Создаем индекс для поля name
    __table_args__ = (Index('ix_priorities_name', 'name'), )
