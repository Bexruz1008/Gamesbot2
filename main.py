import os
import asyncio
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import BOT_TOKEN
from handlers.common import common_router
from handlers.games import games_router

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def health(request):
    return web.Response(text="OK")


async def start_web():
    """Render uchun port ochadigan kichik HTTP server"""
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    logger.info("Veb-server ishga tushdi.")


async def set_bot_commands(bot: Bot):
    """Telegram menyusidagi buyruqlar ro'yxatini sozlash"""
    commands = [
        BotCommand(command="game", description="🎮 Mini o'yinlar menyusini ochish"),
        BotCommand(command="rps", description="🪨 Tosh-Qaychi-Qog'oz o'ynash"),
        BotCommand(command="dice", description="🎲 Zar dueli boshlash"),
        BotCommand(command="darts", description="🎯 Darts (Nishon) dueli"),
        BotCommand(command="basket", description="🏀 Basketbol dueli"),
        BotCommand(command="football", description="⚽ Futbol penalti dueli"),
        BotCommand(command="duel", description="⚔️ Foydalanuvchiga duel e'lon qilish"),
        BotCommand(command="penalties", description="😈 Jazolar ro'yxatini ko'rish"),
        BotCommand(command="help", description="📖 Qo'llanmani ko'rish"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main():
    if not BOT_TOKEN:
        logger.error("XATOLIK: BOT_TOKEN topilmadi! Environment o'zgaruvchisini tekshiring.")
        return

    logger.info("Bot ishga tushirilmoqda...")

    # Render port topishi uchun veb-serverni birinchi ishga tushiramiz
    await start_web()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni ulash
    dp.include_router(common_router)
    dp.include_router(games_router)

    # Buyruqlar menyusini o'rnatish
    try:
        await set_bot_commands(bot)
        logger.info("Bot buyruqlar menyusi muvaffaqiyatli yuklandi.")
    except Exception as e:
        logger.warning(f"Buyruqlarni o'rnatishda xatolik: {e}")

    # Pollingni boshlash
    logger.info("Bot tayyor va xabarlarni kutmoqda!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi.")