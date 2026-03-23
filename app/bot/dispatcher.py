from aiogram import Bot, Dispatcher

from app.bot.handlers.common import router as common_router
from app.core.config import get_settings


def create_dispatcher() -> tuple[Bot, Dispatcher]:
    settings = get_settings()
    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(common_router)
    return bot, dispatcher


async def run_polling() -> None:
    bot, dispatcher = create_dispatcher()
    await dispatcher.start_polling(bot)
