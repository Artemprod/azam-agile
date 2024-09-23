from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at








class Priority(ModelBase):
    __tablename__ = 'priorities'
    id: Mapped[intpk]
    name: Mapped[str]


    projects: Mapped[list["Project"]] = relationship(back_populates="status")

    tasks: Mapped[list["Task"]] = relationship(back_populates="status")


