from datetime import datetime
from typing import Optional, List

from sqlalchemy import Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at


class Project(ModelBase):
    __tablename__ = 'projects'
    project_id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[Optional[str]]
    start_date: Mapped[datetime]
    deadline: Mapped[Optional[datetime]]
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"))

    tasks: Mapped[List["Task"]] = relationship(back_populates="project")
    reports: Mapped[List["Report"]] = relationship(back_populates="project")
    chat: Mapped[Optional["Chat"]] = relationship(back_populates="project", uselist=False)
    owner: Mapped["User"] = relationship(back_populates="projects_owned")
    status:Mapped["Status"] = relationship(back_populates="projects")
    priority:Mapped["Priority"] = relationship(back_populates="projects")

    assigned_users: Mapped[list["User"]] = relationship(
        back_populates="project_assigned",
        secondary="project_assigned"
    )
