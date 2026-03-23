from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import BigInteger, Boolean, DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SubscriptionMode(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    subscription_mode: Mapped[SubscriptionMode] = mapped_column(
        SqlEnum(SubscriptionMode, name="subscription_mode_enum", values_callable=lambda enum: [i.value for i in enum]),
        default=SubscriptionMode.WEEKLY,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    deliveries = relationship("Delivery", back_populates="user", cascade="all, delete-orphan")
