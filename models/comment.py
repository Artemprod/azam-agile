from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at






class Comment(ModelBase):
    __tablename__ = 'comments'
    comment_id: Mapped[intpk]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.project_id"))
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.task_id"))

    user: Mapped["User"] = relationship()
    project: Mapped[Optional["Project"]] = relationship()
    task: Mapped[Optional["Task"]] = relationship()
