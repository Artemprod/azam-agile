
from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at




class Chat(ModelBase):
    __tablename__ = 'chats'
    chat_id: Mapped[intpk]

    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.project_id"))
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.task_id"))

    project: Mapped[Optional["Project"]] = relationship(back_populates="chat")
    task: Mapped[Optional["Task"]] = relationship(back_populates="chat")
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
