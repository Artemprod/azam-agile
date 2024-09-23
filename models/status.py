from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at





class Status(ModelBase):
    __tablename__ = 'statuses'
    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[str]  # "project" или "task"

    # Проекты, которым назначен статус
    projects: Mapped[list["Project"]] = relationship(back_populates="status")

    # Задачи, которым назначен статус
    tasks: Mapped[list["Task"]] = relationship(back_populates="status")

