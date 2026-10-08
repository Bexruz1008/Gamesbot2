# 🎮 Telegram Mini O'yinlar va Jazolar Boti (Python aiogram 3)

Telegram guruhlarida turli qiziqarli mini-o'yinlar (Tosh-qaychi-qog'oz, Zar, Darts, Basketbol, Futbol) o'ynash va mag'lub bo'lgan ishtirokchiga tasodifiy kulgili jazo/topshiriq berish uchun yaratilgan bot.

---

## 🚀 Xususiyatlari

- **🪨✂️📄 Tosh-Qaychi-Qog'oz:**
  - 1v1 duel tizimi.
  - Har ikki ishtirokchi o'z tanlovini sir saqlagan holda inline tugmalar orqali qiladi.
  - Ikkala tomon tanlagach, natija e'lon qilinadi.
  - Durang bo'lsa avtomatik qayta tanlash imkoniyati.
- **🎲 Telegram Zar va Emoji Duellari:**
  - 🎲 **Zar (Dice)** — kimga yuqori raqam tushsa g'olib bo'ladi.
  - 🎯 **Darts (Nishon)** — nishon markaziga eng yaqin tekkan yutadi.
  - 🏀 **Basketbol** — to'pni savatga tushirish bahsi.
  - ⚽ **Futbol penalti** — to'pni darvozaga kiritish bahsi.
  - Telegram'ning haqiqiy animatsiyali emojilaridan foydalaniladi (natijalar Telegram API orqali adolatli belgilanadi).
- **⚡️ Kulgili Jazo va Topshiriqlar Tizimi:**
  - Mag'lub bo'lgan ishtirokchiga bot avtomatik tarzda boyitilgan bazadan tasodifiy kulgili, qiziqarli va xavfsiz vazifa beradi (masalan: kulgili ovozda audio yozish, guruhdagilarga kompliment aytish, she'r to'qish va h.k.).
- **👥 Guruhda chaqirish usullari:**
  - **Ochiq duel:** Guruhda buyruq yuboriladi va har qanday xohlovchi "Duelni qabul qilish" tugmasini bosib o'yinga kiradi.
  - **Aniq ishtirokchiga duel:** Biror kishining xabariga **Reply** qilib buyruq yuborilsa, duel faqat o'sha shaxsga yo'naltiriladi.

---

## 📋 Guruh Buyruqlari

| Buyruq | Tavsif |
|---|---|
| `/game` yoki `/games` | Barcha mini-o'yinlar interaktiv menyusini ochish |
| `/rps` yoki `/tosh` | Tosh-Qaychi-Qog'oz duelini boshlash |
| `/dice` yoki `/zar` | 🎲 Zar duelini boshlash |
| `/darts` yoki `/nishon` | 🎯 Darts (nishon) duelini boshlash |
| `/basket` | 🏀 Basketbol duelini boshlash |
| `/football` yoki `/futbol` | ⚽ Futbol penalti duelini boshlash |
| `/duel` | Foydalanuvchiga duel e'lon qilish menyusi |
| `/penalties` | Botdagi qiziqarli jazolar namunasini ko'rish |
| `/help` | Botdan foydalanish qo'llanmasi |

---

## 🛠 O'rnatish va Ishga Tushirish

### 1. Talablar
- Python 3.9 yoki undan yuqori
- Telegram BotFather dan olingan bot tokeni

### 2. Bog'liqliklarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Sozlash (.env)
Loyihada `.env` faylini yarating (yoki `.env.example` dan nusxa oling):
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxyz
```

> **Bot tokenini olish:** Telegram'da [@BotFather](https://t.me/BotFather) botiga kiring, `/newbot` buyrug'ini yuboring va berilgan tokenni `.env` fayliga yozing.
> **Muhim eslatma:** Guruhlarda o'yinlarni boshqarish uchun BotFather'da `/setprivacy` ni `Disable` qilishingiz yoki botga xabarlarni o'qish imkonini berishingiz tavsiya etiladi.

### 4. Botni ishga tushirish
```bash
python main.py
```

---

## 📁 Loyiha Strukturasi

```text
├── .env.example          # Namuna konfiguratsiya fayli
├── requirements.txt      # Kutubxonalar ro'yxati (aiogram 3.x, python-dotenv)
├── config.py             # Sozlamalar va token boshqaruvi
├── penalties.py          # Qiziqarli jazolar va topshiriqlar ro'yxati
├── games_manager.py      # O'yinlar sessiyasi va holatlarini boshqarish
├── keyboards.py          # Inline tugmalar va klaviaturalar
├── handlers/
│   ├── __init__.py
│   ├── common.py         # /start, /help, /games menyusi
│   └── games.py          # Barcha mini-o'yinlar mantiqi va duel oqimi
├── main.py               # Botning asosiy ishga tushirish nuqtasi
└── README.md             # Qo'llanma
```
