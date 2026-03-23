"""slice1 foundation

Revision ID: 20260323_0001
Revises:
Create Date: 2026-03-23 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260323_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


subscription_mode_enum = sa.Enum("daily", "weekly", name="subscription_mode_enum")
delivery_type_enum = sa.Enum(
    "onboarding",
    "settings_change",
    "about",
    "today_stub",
    "weekly_stub",
    name="delivery_type_enum",
)
delivery_status_enum = sa.Enum("queued", "sent", "failed", name="delivery_status_enum")


def upgrade() -> None:
    subscription_mode_enum.create(op.get_bind(), checkfirst=True)
    delivery_type_enum.create(op.get_bind(), checkfirst=True)
    delivery_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("telegram_user_id", sa.BigInteger(), nullable=False),
        sa.Column("telegram_chat_id", sa.BigInteger(), nullable=False),
        sa.Column("subscription_mode", subscription_mode_enum, nullable=False, server_default="weekly"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("telegram_user_id", name="uq_users_telegram_user_id"),
    )
    op.create_index("ix_users_telegram_user_id", "users", ["telegram_user_id"], unique=False)
    op.create_index("ix_users_telegram_chat_id", "users", ["telegram_chat_id"], unique=False)

    op.create_table(
        "deliveries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("issue_id", sa.Integer(), nullable=True),
        sa.Column("telegram_message_id", sa.Integer(), nullable=True),
        sa.Column("delivery_type", delivery_type_enum, nullable=False),
        sa.Column("section", sa.String(length=100), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("status", delivery_status_enum, nullable=False, server_default="sent"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_deliveries_user_id", "deliveries", ["user_id"], unique=False)
    op.create_index("ix_deliveries_delivery_type", "deliveries", ["delivery_type"], unique=False)
    op.create_index("ix_deliveries_user_id_sent_at", "deliveries", ["user_id", "sent_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_deliveries_user_id_sent_at", table_name="deliveries")
    op.drop_index("ix_deliveries_delivery_type", table_name="deliveries")
    op.drop_index("ix_deliveries_user_id", table_name="deliveries")
    op.drop_table("deliveries")

    op.drop_index("ix_users_telegram_chat_id", table_name="users")
    op.drop_index("ix_users_telegram_user_id", table_name="users")
    op.drop_table("users")

    delivery_status_enum.drop(op.get_bind(), checkfirst=True)
    delivery_type_enum.drop(op.get_bind(), checkfirst=True)
    subscription_mode_enum.drop(op.get_bind(), checkfirst=True)
