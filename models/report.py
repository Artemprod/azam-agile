from datetime import datetime
from typing import Optional, List

from sqlalchemy import  Text, TIMESTAMP, Integer, Boolean, ForeignKey, DateTime, BigInteger, Index, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import ModelBase, intpk, created_at






class Report(ModelBase):
    __tablename__ = 'reports'
    report_id: Mapped[intpk] = mapped_column(index=True)  # Добавляем индекс на поле report_id
    title: Mapped[str]  # Индексируем поле title
    content: Mapped[Optional[str]]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.project_id"), index=True)  # Добавляем индекс на поле project_id
    created_at: Mapped[created_at]

    project: Mapped["Project"] = relationship(back_populates="reports")

    # Создаем индексы для полей title и created_at
    __table_args__ = (
        Index('ix_reports_title', 'title'),

    )