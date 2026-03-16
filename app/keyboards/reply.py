from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗳 Ovoz berish")],
            [KeyboardButton(text="🔗 Mening linkim"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="🏆 Reyting"), KeyboardButton(text="ℹ️ Loyiha haqida")],
        ],
        resize_keyboard=True,
    )


def admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Admin statistika")],
            [KeyboardButton(text="👥 Top referralchilar")],
        ],
        resize_keyboard=True,
    )
