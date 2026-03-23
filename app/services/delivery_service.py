from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Delivery, DeliveryStatus, DeliveryType, User


class DeliveryService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user: User,
        delivery_type: DeliveryType,
        telegram_message_id: int | None,
        status: DeliveryStatus = DeliveryStatus.SENT,
        section: str | None = None,
    ) -> Delivery:
        delivery = Delivery(
            user_id=user.id,
            delivery_type=delivery_type,
            telegram_message_id=telegram_message_id,
            status=status,
            section=section,
        )
        self.session.add(delivery)
        await self.session.commit()
        await self.session.refresh(delivery)
        return delivery
