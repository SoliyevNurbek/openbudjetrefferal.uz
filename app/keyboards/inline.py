from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.config import settings


def vote_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Rasmiy sahifada ovoz berish", url=settings.openbudget_url)]
        ]
    )


def my_referral_keyboard(user_id: int) -> InlineKeyboardMarkup:
    referral_link = f"https://t.me/{settings.bot_username}?start=ref_{user_id}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Mening referral linkim", url=referral_link)],
            [InlineKeyboardButton(text="🗳 Ovoz berish sahifasi", url=settings.openbudget_url)],
        ]
    )
