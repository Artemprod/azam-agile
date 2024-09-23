from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class ProjectAssigned(ModelBase):
    __tablename__ = 'project_assigned'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.user_id',
                   ondelete="CASCADE"),
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('projects.project_id',
                   ondelete="CASCADE"),
        primary_key=True,

    )

    created_at: Mapped[created_at]


class TaskAssigned(ModelBase):
    __tablename__ = 'task_assigned'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.user_id',
                   ondelete="CASCADE"),
        primary_key=True
    )

    research_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('tasks.task_id',
                   ondelete="CASCADE"),
        primary_key=True,

    )

    created_at: Mapped[created_at]
