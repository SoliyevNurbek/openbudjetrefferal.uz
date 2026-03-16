from aiogram import Router, F
from aiogram.types import Message

from app.keyboards.inline import vote_keyboard, my_referral_keyboard
from app.services import runtime
from app.services.stats import build_top_text, build_user_stats_text
from app.utils.texts import ABOUT_TEXT, HOW_TO_VOTE_TEXT, REFERRAL_INFO_TEXT

router = Router()


@router.message(F.text == "🗳 Ovoz berish")
async def vote_handler(message: Message) -> None:
    await message.answer(HOW_TO_VOTE_TEXT, reply_markup=vote_keyboard())


@router.message(F.text == "🔗 Mening linkim")
async def my_link_handler(message: Message) -> None:
    user = message.from_user
    assert user is not None
    await message.answer(REFERRAL_INFO_TEXT, reply_markup=my_referral_keyboard(user.id))


@router.message(F.text == "📊 Statistika")
async def stats_handler(message: Message) -> None:
    db = runtime.DB
    user = message.from_user
    if db is None or user is None:
        await message.answer("Statistika hozircha mavjud emas.")
        return

    text = await build_user_stats_text(db, user.id)
    await message.answer(text)


@router.message(F.text == "🏆 Reyting")
async def ranking_handler(message: Message) -> None:
    db = runtime.DB
    if db is None:
        await message.answer("Reytingni olishda xatolik.")
        return

    text = await build_top_text(db)
    await message.answer(text)


@router.message(F.text == "ℹ️ Loyiha haqida")
async def about_handler(message: Message) -> None:
    await message.answer(ABOUT_TEXT)
