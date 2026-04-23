from datetime import datetime

from sqlalchemy import DateTime, Float, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class AnalysisRecord(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    article_text: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(String(16), nullable=False)
    verdict: Mapped[str] = mapped_column(String(64), nullable=False)
    risk_band: Mapped[str] = mapped_column(String(32), nullable=False)
    fake_probability: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_percent: Mapped[float] = mapped_column(Float, nullable=False)
    word_count: Mapped[int] = mapped_column(nullable=False)
    reading_time_minutes: Mapped[int] = mapped_column(nullable=False)
    character_count: Mapped[int] = mapped_column(nullable=False)
    warning_badges: Mapped[list[dict[str, object]]] = mapped_column(JSON, nullable=False, default=list)
    advisory_note: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String(32), nullable=False, default="manual")
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
