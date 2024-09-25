from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at

class User(ModelBase):
    __tablename__ = 'users'
    user_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле user_id
    name: Mapped[str]  # Индексируем поле name
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)  # Индексируем поле email (unique)
    role_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"), index=True)  # Добавляем индекс на поле role_id
    registration_date: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)  # Индексируем поле registration_date
    avatar: Mapped[Optional[str]]
    created_at: Mapped[created_at]  # Индексируем поле created_at

    projects_owned: Mapped[List["Project"]] = relationship(back_populates="owner")
    role: Mapped["AccessLevel"] = relationship(back_populates="users")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
    project_assigned: Mapped[List["Project"]] = relationship(
        back_populates="assigned_users",
        secondary="project_assigned"
    )
    tasks_assigned: Mapped[List["Task"]] = relationship(
        back_populates="assigned_users",
        secondary="task_assigned"
    )

    # Создаем индексы для полей name и registration_date
    __table_args__ = (
        Index('ix_users_name', 'name'),)