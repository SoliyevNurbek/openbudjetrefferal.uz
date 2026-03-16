from app.services.db import Database


async def build_user_stats_text(db: Database, telegram_id: int) -> str:
    count = await db.get_user_referral_count(telegram_id)
    return (
        "<b>Sizning statistikangiz</b>\n\n"
        f"• Taklif qilgan odamlar soni: <b>{count}</b>\n"
        "• Referral linkingiz orqali kirganlar shu yerda hisoblanadi."
    )


async def build_top_text(db: Database, limit: int = 10) -> str:
    top = await db.get_top_referrers(limit=limit)
    if not top:
        return "Hozircha reyting bo'sh."

    lines = ["<b>Top referralchilar</b>", ""]
    for idx, item in enumerate(top, start=1):
        name = item["full_name"] or "Noma'lum"
        username = f"@{item['username']}" if item.get("username") else "username yo'q"
        lines.append(f"{idx}. {name} ({username}) — <b>{item['referral_count']}</b> ta")
    return "\n".join(lines)


async def build_admin_stats_text(db: Database) -> str:
    stats = await db.get_general_stats()
    return (
        "<b>Admin statistikasi</b>\n\n"
        f"• Jami foydalanuvchilar: <b>{stats['users']}</b>\n"
        f"• Faol foydalanuvchilar: <b>{stats['active_users']}</b>\n"
        f"• Jami referral: <b>{stats['referrals']}</b>"
    )
