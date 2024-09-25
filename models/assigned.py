from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class ProjectAssigned(ModelBase):
    __tablename__ = 'project_assigned'
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.user_id', ondelete="CASCADE"),
        primary_key=True,
        index=True  # Добавляем индекс на поле user_id
    )
    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('projects.project_id', ondelete="CASCADE"),
        primary_key=True,
        index=True  # Добавляем индекс на поле project_id
    )
    created_at: Mapped[created_at]

    # Создаем составной индекс для полей user_id и project_id
    __table_args__ = (Index('ix_project_assigned_user_project', 'user_id', 'project_id'),)


class TaskAssigned(ModelBase):
    __tablename__ = 'task_assigned'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.user_id', ondelete="CASCADE"),
        primary_key=True,
        index=True  # Добавляем индекс на поле user_id
    )
    task_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('tasks.task_id', ondelete="CASCADE"),
        primary_key=True,
        index=True  # Добавляем индекс на поле task_id
    )
    created_at: Mapped[created_at]

    # Создаем составной индекс для полей user_id и task_id
    __table_args__ = (Index('ix_task_assigned_user_task', 'user_id', 'task_id'),)
