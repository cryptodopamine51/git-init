from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

BUTTON_DAILY = "Каждый день"
BUTTON_WEEKLY = "Только еженедельные сводки"
BUTTON_ABOUT = "О боте"
BUTTON_TODAY = "Сегодня"
BUTTON_WEEK_SUMMARY = "Итоги недели"
BUTTON_SETTINGS = "Настройки"


def onboarding_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_DAILY)],
            [KeyboardButton(text=BUTTON_WEEKLY)],
            [KeyboardButton(text=BUTTON_ABOUT)],
        ],
        resize_keyboard=True,
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_TODAY), KeyboardButton(text=BUTTON_WEEK_SUMMARY)],
            [KeyboardButton(text=BUTTON_SETTINGS), KeyboardButton(text=BUTTON_ABOUT)],
        ],
        resize_keyboard=True,
    )


def settings_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BUTTON_DAILY)], [KeyboardButton(text=BUTTON_WEEKLY)]],
        resize_keyboard=True,
    )
