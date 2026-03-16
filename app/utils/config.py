import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    bot_username: str
    openbudget_url: str
    admin_ids: list[int]
    database_path: str



def _parse_admin_ids(raw: str) -> list[int]:
    if not raw.strip():
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


settings = Settings(
    bot_token=os.getenv("BOT_TOKEN", ""),
    bot_username=os.getenv("BOT_USERNAME", ""),
    openbudget_url=os.getenv("OPENBUDGET_URL", "https://openbudget.uz/"),
    admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
    database_path=os.getenv("DATABASE_PATH", "data/bot.db"),
)

if not settings.bot_token:
    raise ValueError("BOT_TOKEN topilmadi. .env faylni to'ldiring.")
