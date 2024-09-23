from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at








class Message(ModelBase):
    __tablename__ = 'messages'
    message_id: Mapped[intpk]
    content: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    sent_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship(back_populates="messages")

