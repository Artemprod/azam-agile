from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at




class Notification(ModelBase):
    __tablename__ = 'notifications'
    id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле id
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)  # Добавляем индекс на поле user_id
    sent_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)  # Добавляем индекс на поле sent_at
    user: Mapped["User"] = relationship(back_populates="notifications")

    # Создаем составной индекс для полей user_id и sent_at
    __table_args__ = (
        Index('ix_notifications_user_sent_at', 'user_id', 'sent_at'),
    )