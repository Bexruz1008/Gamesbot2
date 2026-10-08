import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    # Ogohlantirish: token mavjud emas bo'lsa
    print("OGOHLANTIRISH: BOT_TOKEN topilmadi! Iltimos, .env faylida BOT_TOKEN ni belgilang.")
