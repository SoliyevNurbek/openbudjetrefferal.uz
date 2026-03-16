from app.services.db import Database


async def process_referral(db: Database, referred_user_id: int, referrer_user_id: int | None) -> str | None:
    if not referrer_user_id:
        return None

    if referred_user_id == referrer_user_id:
        return "O'zingizni o'zingiz referral qila olmaysiz."

    referrer_exists = await db.has_user(referrer_user_id)
    if not referrer_exists:
        return "Referral egasi bazada topilmadi."

    added = await db.add_referral(referrer_user_id, referred_user_id)
    if not added:
        return "Siz avval ham referral sifatida ro'yxatdan o'tgansiz."

    return "Referral muvaffaqiyatli qabul qilindi."



def parse_referrer(args: str | None) -> int | None:
    if not args:
        return None

    args = args.strip()
    if not args.startswith("ref_"):
        return None

    raw_id = args.replace("ref_", "", 1)
    if not raw_id.isdigit():
        return None

    return int(raw_id)
