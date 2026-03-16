from aiogram import Router, F
from aiogram.types import Message

from app.services import runtime
from app.services.stats import build_admin_stats_text, build_top_text
from app.utils.config import settings

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(F.text == "📈 Admin statistika")
async def admin_stats_handler(message: Message) -> None:
    user = message.from_user
    if user is None or not is_admin(user.id):
        return

    db = runtime.DB
    if db is None:
        await message.answer("Admin statistika mavjud emas.")
        return

    text = await build_admin_stats_text(db)
    await message.answer(text)


@router.message(F.text == "👥 Top referralchilar")
async def admin_top_handler(message: Message) -> None:
    user = message.from_user
    if user is None or not is_admin(user.id):
        return

    db = runtime.DB
    if db is None:
        await message.answer("Ma'lumotni olishda xatolik.")
        return

    text = await build_top_text(db, limit=20)
    await message.answer(text)
