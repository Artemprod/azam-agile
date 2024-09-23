from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class Task(ModelBase):
    __tablename__ = 'tasks'
    task_id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[Optional[str]]
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    executor_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"))
    deadline: Mapped[Optional[datetime]]

    priority: Mapped["Priority"] = relationship(back_populates="tasks")
    chat: Mapped[Optional["Chat"]] = relationship(back_populates="task", uselist=False)
    project: Mapped["Project"] = relationship(back_populates="tasks")
    executor: Mapped["User"] = relationship(back_populates="tasks_assigned")
    status: Mapped["Status"] = relationship(back_populates="tasks")

    assigned_users: Mapped[list["User"]] = relationship(
        back_populates="tasks_assigned",
        secondary="task_assigned"
    )
