from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at




class Notification(ModelBase):
    __tablename__ = 'notifications'
    id: Mapped[intpk]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    sent_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="notifications")

