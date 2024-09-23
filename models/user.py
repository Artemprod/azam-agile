from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at

class User(ModelBase):
    __tablename__ = 'users'

    user_id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"))
    registration_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    avatar: Mapped[Optional[str]]
    created_at: Mapped[created_at]

    projects_owned: Mapped[List["Project"]] = relationship(back_populates="owner")
    access_level: Mapped["AccessLevel"] = relationship(back_populates="users")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="user")

    project_assigned: Mapped[list["Project"]] = relationship(
        back_populates="assigned_users",
        secondary="project_assigned"
    )

    tasks_assigned: Mapped[list["Task"]] = relationship(
        back_populates="assigned_users",
        secondary="task_assigned"
    )
