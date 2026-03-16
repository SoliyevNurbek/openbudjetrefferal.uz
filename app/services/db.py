import os
import sqlite3
from typing import Any


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self.conn: sqlite3.Connection | None = None

    async def connect(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row

    async def init_tables(self) -> None:
        assert self.conn is not None
        cursor = self.conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                full_name TEXT,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_telegram_id INTEGER NOT NULL,
                referred_telegram_id INTEGER UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            """
        )
        self.conn.commit()

    async def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        assert self.conn is not None
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    async def fetchone(self, query: str, params: tuple = ()) -> sqlite3.Row | None:
        cur = await self.execute(query, params)
        return cur.fetchone()

    async def fetchall(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        cur = await self.execute(query, params)
        return cur.fetchall()

    async def get_or_create_user(self, telegram_id: int, full_name: str, username: str | None) -> None:
        existing = await self.fetchone(
            "SELECT telegram_id FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        if existing:
            await self.execute(
                """
                UPDATE users
                SET full_name = ?, username = ?, is_active = 1
                WHERE telegram_id = ?
                """,
                (full_name, username, telegram_id),
            )
            return

        await self.execute(
            "INSERT INTO users (telegram_id, full_name, username) VALUES (?, ?, ?)",
            (telegram_id, full_name, username),
        )

    async def add_referral(self, referrer_telegram_id: int, referred_telegram_id: int) -> bool:
        existing = await self.fetchone(
            "SELECT id FROM referrals WHERE referred_telegram_id = ?",
            (referred_telegram_id,),
        )
        if existing:
            return False

        await self.execute(
            "INSERT INTO referrals (referrer_telegram_id, referred_telegram_id) VALUES (?, ?)",
            (referrer_telegram_id, referred_telegram_id),
        )
        return True

    async def has_user(self, telegram_id: int) -> bool:
        row = await self.fetchone(
            "SELECT telegram_id FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        return row is not None

    async def get_user_referral_count(self, telegram_id: int) -> int:
        row = await self.fetchone(
            "SELECT COUNT(*) AS cnt FROM referrals WHERE referrer_telegram_id = ?",
            (telegram_id,),
        )
        return int(row["cnt"]) if row else 0

    async def get_top_referrers(self, limit: int = 10) -> list[dict[str, Any]]:
        rows = await self.fetchall(
            """
            SELECT
                u.telegram_id,
                u.full_name,
                u.username,
                COUNT(r.id) AS referral_count
            FROM users u
            LEFT JOIN referrals r ON r.referrer_telegram_id = u.telegram_id
            GROUP BY u.telegram_id, u.full_name, u.username
            ORDER BY referral_count DESC, u.joined_at ASC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in rows]

    async def get_general_stats(self) -> dict[str, int]:
        users_row = await self.fetchone("SELECT COUNT(*) AS cnt FROM users")
        active_row = await self.fetchone("SELECT COUNT(*) AS cnt FROM users WHERE is_active = 1")
        referrals_row = await self.fetchone("SELECT COUNT(*) AS cnt FROM referrals")
        return {
            "users": int(users_row["cnt"]) if users_row else 0,
            "active_users": int(active_row["cnt"]) if active_row else 0,
            "referrals": int(referrals_row["cnt"]) if referrals_row else 0,
        }
