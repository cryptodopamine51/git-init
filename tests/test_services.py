from app.services.about_service import get_about_text
from app.services.user_service import UserService
from app.db.models import SubscriptionMode


async def test_create_user_on_start(db_session):
    service = UserService(db_session)
    user, created = await service.get_or_create_user(telegram_user_id=1, telegram_chat_id=100)

    assert created is True
    assert user.telegram_user_id == 1


async def test_save_daily_subscription_mode(db_session):
    service = UserService(db_session)
    user, _ = await service.get_or_create_user(telegram_user_id=2, telegram_chat_id=101)

    updated = await service.set_subscription_mode(user, SubscriptionMode.DAILY)

    assert updated.subscription_mode == SubscriptionMode.DAILY


async def test_save_weekly_subscription_mode(db_session):
    service = UserService(db_session)
    user, _ = await service.get_or_create_user(telegram_user_id=3, telegram_chat_id=102)

    updated = await service.set_subscription_mode(user, SubscriptionMode.WEEKLY)

    assert updated.subscription_mode == SubscriptionMode.WEEKLY


async def test_repeat_start_existing_user(db_session):
    service = UserService(db_session)
    first, created_first = await service.get_or_create_user(telegram_user_id=4, telegram_chat_id=103)
    second, created_second = await service.get_or_create_user(telegram_user_id=4, telegram_chat_id=104)

    assert created_first is True
    assert created_second is False
    assert first.id == second.id
    assert second.telegram_chat_id == 104


async def test_change_mode_in_settings(db_session):
    service = UserService(db_session)
    user, _ = await service.get_or_create_user(telegram_user_id=5, telegram_chat_id=105)
    await service.set_subscription_mode(user, SubscriptionMode.DAILY)

    updated = await service.set_subscription_mode(user, SubscriptionMode.WEEKLY)

    assert updated.subscription_mode == SubscriptionMode.WEEKLY


def test_about_text_render_contains_required_sections():
    about = get_about_text()

    assert "Что это" in about
    assert "Важное" in about
    assert "Новости ИИ" in about
    assert "Кодинг" in about
    assert "Инвестиции" in about
    assert "Альфа" in about
