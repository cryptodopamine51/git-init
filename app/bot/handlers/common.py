from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from app.bot.keyboards.reply import (
    BUTTON_ABOUT,
    BUTTON_DAILY,
    BUTTON_SETTINGS,
    BUTTON_TODAY,
    BUTTON_WEEK_SUMMARY,
    BUTTON_WEEKLY,
    main_menu_keyboard,
    onboarding_keyboard,
    settings_keyboard,
)
from app.bot.texts import (
    DAILY_CONFIRMATION_TEXT,
    SETTINGS_PROMPT_TEXT,
    TODAY_STUB_TEXT,
    WEEKLY_CONFIRMATION_TEXT,
    WEEKLY_STUB_TEXT,
    WELCOME_TEXT,
)
from app.db.models import DeliveryType, SubscriptionMode
from app.db.session import SessionLocal
from app.services.about_service import get_about_text
from app.services.delivery_service import DeliveryService
from app.services.user_service import UserService

router = Router()


class OnboardingState(StatesGroup):
    waiting_mode = State()


class SettingsState(StatesGroup):
    waiting_mode = State()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    async with SessionLocal() as session:
        user_service = UserService(session)
        await user_service.get_or_create_user(
            telegram_user_id=message.from_user.id,
            telegram_chat_id=message.chat.id,
        )

    await state.set_state(OnboardingState.waiting_mode)
    await message.answer(WELCOME_TEXT, reply_markup=onboarding_keyboard())


@router.message(F.text == BUTTON_SETTINGS)
async def settings_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(SettingsState.waiting_mode)
    await message.answer(SETTINGS_PROMPT_TEXT, reply_markup=settings_keyboard())


@router.message(F.text == BUTTON_ABOUT)
async def about_handler(message: Message) -> None:
    if message.from_user is None:
        return
    async with SessionLocal() as session:
        user_service = UserService(session)
        delivery_service = DeliveryService(session)
        user, _ = await user_service.get_or_create_user(message.from_user.id, message.chat.id)
        sent_message = await message.answer(get_about_text(), reply_markup=main_menu_keyboard())
        await delivery_service.create(user, DeliveryType.ABOUT, sent_message.message_id)


@router.message(F.text == BUTTON_TODAY)
async def today_handler(message: Message) -> None:
    if message.from_user is None:
        return
    async with SessionLocal() as session:
        user_service = UserService(session)
        delivery_service = DeliveryService(session)
        user, _ = await user_service.get_or_create_user(message.from_user.id, message.chat.id)
        sent_message = await message.answer(TODAY_STUB_TEXT)
        await delivery_service.create(user, DeliveryType.TODAY_STUB, sent_message.message_id)


@router.message(F.text == BUTTON_WEEK_SUMMARY)
async def week_summary_handler(message: Message) -> None:
    if message.from_user is None:
        return
    async with SessionLocal() as session:
        user_service = UserService(session)
        delivery_service = DeliveryService(session)
        user, _ = await user_service.get_or_create_user(message.from_user.id, message.chat.id)
        sent_message = await message.answer(WEEKLY_STUB_TEXT)
        await delivery_service.create(user, DeliveryType.WEEKLY_STUB, sent_message.message_id)


@router.message(OnboardingState.waiting_mode, F.text.in_({BUTTON_DAILY, BUTTON_WEEKLY}))
async def onboarding_subscription_handler(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    mode = SubscriptionMode.DAILY if message.text == BUTTON_DAILY else SubscriptionMode.WEEKLY
    confirmation = DAILY_CONFIRMATION_TEXT if mode == SubscriptionMode.DAILY else WEEKLY_CONFIRMATION_TEXT

    async with SessionLocal() as session:
        user_service = UserService(session)
        delivery_service = DeliveryService(session)
        user, _ = await user_service.get_or_create_user(message.from_user.id, message.chat.id)
        await user_service.set_subscription_mode(user, mode)
        sent_message = await message.answer(confirmation, reply_markup=main_menu_keyboard())
        await delivery_service.create(user, DeliveryType.ONBOARDING, sent_message.message_id)

    await state.clear()


@router.message(SettingsState.waiting_mode, F.text.in_({BUTTON_DAILY, BUTTON_WEEKLY}))
async def settings_subscription_handler(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    mode = SubscriptionMode.DAILY if message.text == BUTTON_DAILY else SubscriptionMode.WEEKLY
    confirmation = DAILY_CONFIRMATION_TEXT if mode == SubscriptionMode.DAILY else WEEKLY_CONFIRMATION_TEXT

    async with SessionLocal() as session:
        user_service = UserService(session)
        delivery_service = DeliveryService(session)
        user, _ = await user_service.get_or_create_user(message.from_user.id, message.chat.id)
        await user_service.set_subscription_mode(user, mode)
        sent_message = await message.answer(confirmation, reply_markup=main_menu_keyboard())
        await delivery_service.create(user, DeliveryType.SETTINGS_CHANGE, sent_message.message_id)

    await state.clear()
