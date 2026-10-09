import html
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from penalties import PENALTIES
from keyboards import get_games_menu_keyboard

common_router = Router()

START_TEXT = """
👋 <b>Assalomu alaykum!</b>

Men guruhlar uchun <b>Mini O'yinlar va Jazolar</b> botiman! 🎮

Meni guruhingizga qo'shing va do'stlaringiz bilan turli qiziqarli o'yinlar o'ynab, yutqazganlarga kulgili shartlar bering!

<b>🔥 Mavjud o'yinlar:</b>
• 🪨✂️📄 <b>Tosh-Qaychi-Qog'oz</b> — klassik duel
• 🎲 <b>Zar dueli</b> — kim ko'p ball olsa o'sha yutadi
• 🎯 <b>Darts (Nishon)</b> — aniqlik bo'yicha bahs
• 🏀 <b>Basketbol</b> — savatga to'p tushirish
• ⚽ <b>Futbol</b> — penalti seriyasi

<b>⚡️ Yutqazgan nima qiladi?</b>
Har bir o'yinda mag'lub bo'lgan ishtirokchiga bot tasodifiy qiziqarli topshiriq (audio yozish, latifa aytish, she'r to'qish va h.k.) beradi!

Guruhda o'yin boshlash uchun /game yoki /help buyrug'ini yuboring!
"""

HELP_TEXT = """
📖 <b>Botdan guruhda foydalanish qo'llanmasi:</b>

1️⃣ <b>Botni guruhga qo'shing</b> (admin qilish shart emas, lekin tavsiya etiladi).
2️⃣ Guruhda quyidagi buyruqlardan birini yuboring:

<b>🎮 O'yin buyruqlari:</b>
• <code>/game</code> yoki <code>/games</code> — O'yin tanlash menyusi
• <code>/rps</code> — Tosh-Qaychi-Qog'oz duelini boshlash
• <code>/dice</code> — 🎲 Zar duelini boshlash
• <code>/darts</code> — 🎯 Nishon duelini boshlash
• <code>/basket</code> — 🏀 Basketbol duelini boshlash
• <code>/football</code> — ⚽ Futbol duelini boshlash
• <code>/duel</code> — Biror kishiga duel e'lon qilish

<b>💡 Duelga chaqirish usullari:</b>
• <b>Ochiq duel:</b> Shunchaki <code>/game</code> yoki <code>/rps</code> yuboring, xohlovchi har qanday kishi "Qabul qilish"ni bosishi mumkin.
• <b>Aniq odamga duel:</b> Biror kishining xabariga <b>Reply (Javob)</b> qilib buyruqni yuboring!

<b>⚡️ Jazolar haqida:</b>
• <code>/penalties</code> — Botdagi qiziqarli jazolar va shartlar namunasini ko'rish.
"""

@common_router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.type in ("group", "supergroup"):
        await message.reply(
            f"🎮 Salom, {html.escape(message.from_user.full_name)}! O'yin boshlash uchun /game buyrug'ini yuboring.",
            parse_mode="HTML"
        )
    else:
        await message.answer(START_TEXT, parse_mode="HTML")

@common_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(HELP_TEXT, parse_mode="HTML")

@common_router.message(Command("penalties"))
async def cmd_penalties(message: Message):
    penalties_preview = "\n\n".join([f"• {p}" for p in PENALTIES[:7]])
    text = f"""
😈 <b>Botdagi qiziqarli jazo va shartlardan namunalar:</b>

{penalties_preview}

<i>...va yana ko'plab boshqa kulgili topshiriqlar mavjud! Yutqazmaslikka harakat qiling! 😉</i>
"""
    await message.reply(text, parse_mode="HTML")

@common_router.message(Command(commands=["game", "games"]))
async def cmd_game_menu(message: Message):
    target_id = 0
    target_name = None

    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
        if not target.is_bot and target.id != message.from_user.id:
            target_id = target.id
            target_name = target.full_name

    initiator_name = html.escape(message.from_user.full_name)
    
    if target_id and target_name:
        text = (
            f"🎮 <b>DUEL VAQTI!</b>\n"
            f"👤 <b>{initiator_name}</b> ⚔️ <b>{html.escape(target_name)}</b> ga chaqiruv tashladi!\n\n"
            f"Qaysi o'yinni o'ynaysizlar? Quyidan tanlang 👇"
        )
    else:
        text = (
            f"🎮 <b>MINI O'YINLAR MENYUSI</b>\n"
            f"👤 <b>{initiator_name}</b> duel boshlamoqchi!\n\n"
            f"O'yin turini tanlang 👇"
        )

    await message.reply(
        text,
        reply_markup=get_games_menu_keyboard(target_id, message.from_user.id),
        parse_mode="HTML"
    )

@common_router.callback_query(F.data.startswith("close_menu:"))
async def cb_close_menu(callback: CallbackQuery):
    opener_id = int(callback.data.split(":")[1])
    if callback.from_user.id != opener_id:
        await callback.answer("Bu menyuni faqat uni ochgan odam boshqara oladi.", show_alert=True)
        return

    try:
        await callback.message.delete()
    except Exception:
        await callback.answer("Menyu yopildi.")
