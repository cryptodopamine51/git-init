from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DeliveryType(str, Enum):
    ONBOARDING = "onboarding"
    SETTINGS_CHANGE = "settings_change"
    ABOUT = "about"
    TODAY_STUB = "today_stub"
    WEEKLY_STUB = "weekly_stub"


class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"


class Delivery(Base):
    __tablename__ = "deliveries"
    __table_args__ = (
        Index("ix_deliveries_user_id_sent_at", "user_id", "sent_at"),
        Index("ix_deliveries_delivery_type", "delivery_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    issue_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    telegram_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    delivery_type: Mapped[DeliveryType] = mapped_column(
        SqlEnum(DeliveryType, name="delivery_type_enum", values_callable=lambda enum: [i.value for i in enum]),
        nullable=False,
    )
    section: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[DeliveryStatus] = mapped_column(
        SqlEnum(DeliveryStatus, name="delivery_status_enum", values_callable=lambda enum: [i.value for i in enum]),
        default=DeliveryStatus.SENT,
        nullable=False,
    )

    user = relationship("User", back_populates="deliveries")
