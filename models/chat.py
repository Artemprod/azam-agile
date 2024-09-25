
from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at




class Chat(ModelBase):
    __tablename__ = 'chats'
    chat_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле chat_id
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.project_id"), index=True)  # Добавляем индекс на поле project_id
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.task_id"), index=True)  # Добавляем индекс на поле task_id
    project: Mapped[Optional["Project"]] = relationship(back_populates="chat")
    task: Mapped[Optional["Task"]] = relationship(back_populates="chat")
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")

    # Создаем составной индекс для полей project_id и task_id
    __table_args__ = (Index('ix_chat_project_task', 'project_id', 'task_id'), )