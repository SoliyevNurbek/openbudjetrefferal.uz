# OpenBudget Referral Bot

Bu loyiha **OpenBudget uchun qonuniy promo/referral Telegram bot** hisoblanadi. Bot:

- foydalanuvchini referral orqali ro'yxatdan o'tkazadi
- maxsus ovoz berish linkini ulashadi
- referal sonini hisoblaydi
- reytingni ko'rsatadi
- admin uchun statistika beradi
- **hech qanday avtomatik ovoz berish, himoyani chetlab o'tish yoki saytni manipulyatsiya qilish funksiyasini bajarmaydi**

## Arxitektura

```text
Telegram User
    |
    v
Aiogram Bot
    |
    +--> handlers/         # command va callback logikasi
    +--> keyboards/        # reply / inline keyboardlar
    +--> services/         # DB, business logic, stats
    +--> utils/            # config va yordamchi funksiyalar
    |
    v
SQLite Database
    |
    +--> users
    +--> referrals
    +--> settings
```

## Asosiy imkoniyatlar

- `/start` va referral qabul qilish (`/start ref_<telegram_id>`)
- loyiha haqida ma'lumot
- OpenBudget linkini inline tugma bilan berish
- foydalanuvchining shaxsiy referral linki
- top referral reytingi
- foydalanuvchi statistikasi
- admin panel:
  - umumiy userlar soni
  - faol userlar soni
  - referral soni
  - eng ko'p referral qilganlar
  - broadcast uchun tayyor asos

## Tuzilma

```text
openbudget_referral_bot/
├── app/
│   ├── handlers/
│   │   ├── start.py
│   │   ├── menu.py
│   │   └── admin.py
│   ├── keyboards/
│   │   ├── reply.py
│   │   └── inline.py
│   ├── services/
│   │   ├── db.py
│   │   ├── referral.py
│   │   └── stats.py
│   └── utils/
│       ├── config.py
│       └── texts.py
├── data/
│   └── .gitkeep
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

## O'rnatish

### 1. Virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Kutubxonalar

```bash
pip install -r requirements.txt
```

### 3. `.env` yaratish

`.env.example` ni `.env` ga ko'chiring va to'ldiring:

```env
BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=your_bot_username_without_at
OPENBUDGET_URL=https://openbudget.uz/boards/initiatives/initiative/48/123456789012
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/bot.db
```

## Ishga tushirish

```bash
python main.py
```

## Referral ishlash tartibi

1. Foydalanuvchi botga kiradi.
2. Agar u referral link bilan kirgan bo'lsa, masalan:
   `https://t.me/your_bot?start=ref_123456789`
3. Bot refer qilgan userni tekshiradi.
4. Self-referral va dublikat referral bloklanadi.
5. Referral bazaga yoziladi.
6. Har bir foydalanuvchi o'zining referral linkini oladi.

## Eslatma

Bu loyiha promo, monitoring va referral kampaniyasi uchun yozilgan. OpenBudget sahifasiga foydalanuvchini yo'naltiradi, lekin uning o'rniga ovoz bermaydi.
