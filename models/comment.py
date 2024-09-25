from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at






class Comment(ModelBase):
    __tablename__ = 'comments'
    comment_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле comment_id
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)  # Добавляем индекс на поле user_id
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.project_id"), index=True)  # Добавляем индекс на поле project_id
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.task_id"), index=True)  # Добавляем индекс на поле task_id

    user: Mapped["User"] = relationship()
    project: Mapped[Optional["Project"]] = relationship()
    task: Mapped[Optional["Task"]] = relationship()

    # Создаем составной индекс для полей user_id, project_id и task_id
    __table_args__ = (
        Index('ix_comments_user_project', 'user_id', 'project_id'),
        Index('ix_comments_user_task', 'user_id', 'task_id'),
    )