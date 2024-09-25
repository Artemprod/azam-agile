from datetime import datetime
from typing import Optional, List
from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base import ModelBase, intpk, created_at

class Message(ModelBase):
    __tablename__ = 'messages'
    message_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле message_id
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)  # Добавляем индекс на поле user_id
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"), index=True)  # Добавляем индекс на поле chat_id
    sent_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)  # Добавляем индекс на поле sent_at
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship(back_populates="messages")

    # Создаем составной индекс для полей user_id и chat_id
    __table_args__ = (
        Index('ix_messages_user_chat', 'user_id', 'chat_id'),
    )