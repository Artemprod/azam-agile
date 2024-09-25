from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class Task(ModelBase):
    __tablename__ = 'tasks'
    task_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле task_id
    title: Mapped[str]  # Индексируем поле title
    description: Mapped[Optional[str]]
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"), index=True)  # Добавляем индекс на поле priority_id
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), index=True)  # Добавляем индекс на поле status_id
    executor_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)  # Добавляем индекс на поле executor_id
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"), index=True)  # Добавляем индекс на поле project_id
    deadline: Mapped[Optional[datetime]] = mapped_column(index=True)  # Добавляем индекс на поле deadline

    priority: Mapped["Priority"] = relationship(back_populates="tasks")
    chat: Mapped[Optional["Chat"]] = relationship(back_populates="task", uselist=False)
    project: Mapped["Project"] = relationship(back_populates="tasks")
    executor: Mapped["User"] = relationship(back_populates="tasks_assigned")
    status: Mapped["Status"] = relationship(back_populates="tasks")
    assigned_users: Mapped[List["User"]] = relationship(
        back_populates="tasks_assigned",
        secondary="task_assigned"
    )

    # Создаем индексы для полей title и deadline
    __table_args__ = (
        Index('ix_tasks_title', 'title'),
    )