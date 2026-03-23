from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        Index("ix_events_event_date", "event_date"),
        Index("ix_events_importance_score", "importance_score"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    cluster_key: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    event_date: Mapped[date] = mapped_column(Date, nullable=False)
    title: Mapped[str] = mapped_column(String(1024), nullable=False)
    short_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    long_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_source_id: Mapped[int | None] = mapped_column(ForeignKey("sources.id", ondelete="SET NULL"), nullable=True)
    primary_source_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    importance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    market_impact_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ai_news_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    coding_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    investment_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_highlight: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    categories = relationship("EventCategory", back_populates="event", cascade="all, delete-orphan")
    tags = relationship("EventTag", back_populates="event", cascade="all, delete-orphan")
    sources = relationship("EventSource", back_populates="event", cascade="all, delete-orphan")
