from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters.command import CommandObject

from app.keyboards.reply import main_menu, admin_menu
from app.services import runtime
from app.services.referral import parse_referrer, process_referral
from app.utils.config import settings
from app.utils.texts import WELCOME_TEXT

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, command: CommandObject) -> None:
    db = runtime.DB
    if db is None:
        await message.answer("Bot bazasi hali tayyor emas.")
        return

    user = message.from_user
    assert user is not None

    await db.get_or_create_user(
        telegram_id=user.id,
        full_name=user.full_name,
        username=user.username,
    )

    referrer_id = parse_referrer(command.args)
    referral_status = await process_referral(db, user.id, referrer_id)

    text = WELCOME_TEXT
    if referral_status:
        text += f"\n<b>Referral holati:</b> {referral_status}\n"

    await message.answer(text, reply_markup=main_menu())

    if user.id in settings.admin_ids:
        await message.answer("Admin menyu faollashtirildi.", reply_markup=admin_menu())
