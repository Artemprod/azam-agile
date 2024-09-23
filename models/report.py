from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at






class Report(ModelBase):
    __tablename__ = 'reports'
    report_id: Mapped[intpk]
    title: Mapped[str]
    content: Mapped[Optional[str]]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"))
    created_at: Mapped[created_at]

    project: Mapped["Project"] = relationship(back_populates="reports")

