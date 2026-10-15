# 🎮 Telegram Mini O'yinlar Boti (Python aiogram 3)

Telegram guruhlarida turli qiziqarli mini-o'yinlar (Tosh-qaychi-qog'oz, Zar, Darts, Basketbol, Futbol, Bowling, Rus Ruletkasi, Tic-Tac-Toe, Son Topish) o'ynash uchun yaratilgan bot.

---

## 🚀 Xususiyatlari

- **🪨✂️📄 Tosh-Qaychi-Qog'oz:**
  - 1v1 duel tizimi, maxfiy inline tanlov va avtomatik durang qayta tanlash.
- **🎲 Telegram Zar va Emoji Duellari:**
  - 🎲 **Zar (Dice)** — eng yuqori ochko bahsi.
  - 🎯 **Darts (Nishon)** — nishon markaziga aniq tekkazish.
  - 🏀 **Basketbol** — savatga to'p tushirish bahsi.
  - ⚽ **Futbol penalti** — darvozaga to'p kiritish bahsi.
  - 🎳 **Bowling** — keglilarni maksimal qulatish bahsi.
  - Telegram'ning haqiqiy animatsiyali emojilaridan foydalaniladi.
- **💣 Xavfsiz Rus Ruletkasi:**
  - 6 ta patron joyli revolver barabani. O'yinchilar navbatma-navbat tepkini bosishadi, kimda patron chiqsa o'sha mag'lub bo'ladi.
- **❌⭕ Tic-Tac-Toe (Xoch-Doira):**
  - 3x3 interaktiv inline doska, navbatli yurish, g'alaba kombinatsiyalari va durangni aniqlash.
- **🔢 Son Topish (1-100):**
  - Ikkala o'yinchi botda o'z maxfiy sonini belgilaydi (lichkada yoki tasodifiy son tanlash orqali).
  - So'ng guruhda navbat bilan raqib soni taxmin qilinadi, bot "Kattaroq 📈" yoki "Kichikroq 📉" deb yo'naltiradi.
- **🧹 Avto-tozalash (Auto-delete):**
  - O'yin davomida tashlangan zar, darts va oraliq xabarlar 5 daqiqadan so'ng avtomatik o'chib ketadi.
  - G'olib e'lon qilingan yakuniy natija xabari 12 soatdan so'ng guruhdan o'chiriladi.
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
| `/bowling` yoki `/bouling` | 🎳 Bowling duelini boshlash |
| `/roulette` yoki `/ruletka` | 💣 Rus Ruletkasi duelini boshlash |
| `/tictactoe` yoki `/xo` | ❌⭕ Tic-Tac-Toe duelini boshlash |
| `/guess` yoki `/sontop` | 🔢 Son Topish (1-100) duelini boshlash |
| `/duel` | Foydalanuvchiga duel e'lon qilish menyusi |
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
