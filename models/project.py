from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class Project(ModelBase):
    __tablename__ = 'projects'
    project_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле project_id
    title: Mapped[str]  # Индексируем поле title
    description: Mapped[Optional[str]]
    start_date: Mapped[datetime]  # Индексируем поле start_date
    deadline: Mapped[Optional[datetime]]
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"), index=True)  # Добавляем индекс на поле status_id
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)  # Добавляем индекс на поле owner_id
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"), index=True)  # Добавляем индекс на поле priority_id

    tasks: Mapped[List["Task"]] = relationship(back_populates="project")
    reports: Mapped[List["Report"]] = relationship(back_populates="project")
    chat: Mapped[Optional["Chat"]] = relationship(back_populates="project", uselist=False)
    owner: Mapped["User"] = relationship(back_populates="projects_owned")
    status: Mapped["Status"] = relationship(back_populates="projects")
    priority: Mapped["Priority"] = relationship(back_populates="projects")
    assigned_users: Mapped[List["User"]] = relationship(
        back_populates="project_assigned",
        secondary="project_assigned"
    )

    # Создаем индексы для полей title и start_date
    __table_args__ = (
        Index('ix_projects_title', 'title'),
        Index('ix_projects_start_date', 'start_date'),
    )