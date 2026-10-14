import html
from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import get_games_menu_keyboard
from games_manager import games_manager
from handlers.games import schedule_delete_message, GAME_MSG_DELETE_DELAY

common_router = Router()

START_TEXT = """
👋 <b>Assalomu alaykum!</b>

Men guruhlar uchun <b>Mini O'yinlar</b> botiman! 🎮

Meni guruhingizga qo'shing va do'stlaringiz bilan turli qiziqarli o'yinlar o'ynang!

<b>🔥 Mavjud barcha o'yinlar:</b>
• 🪨✂️📄 <b>Tosh-Qaychi-Qog'oz</b> — klassik duel
• 🎲 <b>Zar dueli</b> — yuqori ochko bahsi
• 🎯 <b>Darts (Nishon)</b> — aniqlik bahsi
• 🏀 <b>Basketbol</b> — to'p tushirish
• ⚽ <b>Futbol</b> — penalti seriyasi
• 🎳 <b>Bowling</b> — keglilarni urish
• 💣 <b>Rus Ruletkasi</b> — hayajonli tavakkal o'yini
• ❌⭕ <b>Tic-Tac-Toe</b> — klassik Krestik-Nolik
• 🔢 <b>Son Topish (1-100)</b> — maxfiy sonni topish bahsi

Guruhda o'yin boshlash uchun /game yoki /help buyrug'ini yuboring!
"""

HELP_TEXT = """
📖 <b>Botdan guruhda foydalanish qo'llanmasi:</b>

1️⃣ <b>Botni guruhga qo'shing</b> (admin qilish shart emas).
2️⃣ Guruhda quyidagi buyruqlardan birini yuboring:

<b>🎮 O'yin buyruqlari:</b>
• <code>/game</code> yoki <code>/games</code> — O'yin tanlash menyusi
• <code>/rps</code> — Tosh-Qaychi-Qog'oz
• <code>/dice</code> — 🎲 Zar dueli
• <code>/darts</code> — 🎯 Nishon dueli
• <code>/basket</code> — 🏀 Basketbol dueli
• <code>/football</code> — ⚽ Futbol dueli
• <code>/bowling</code> — 🎳 Bowling dueli
• <code>/roulette</code> — 💣 Rus Ruletkasi
• <code>/tictactoe</code> — ❌⭕ Tic-Tac-Toe
• <code>/guess</code> — 🔢 Son Topish (1-100)
• <code>/duel</code> — Biror kishiga duel e'lon qilish

<b>💡 Duelga chaqirish usullari:</b>
• <b>Ochiq duel:</b> Shunchaki buyruq yuboring, xohlovchi har qanday kishi "Qabul qilish"ni bosishi mumkin.
• <b>Aniq odamga duel:</b> Biror kishining xabariga <b>Reply (Javob)</b> qilib buyruqni yuboring!
"""

@common_router.message(CommandStart())
async def cmd_start(message: Message):
    if message.chat.type in ("group", "supergroup"):
        await message.reply(
            f"🎮 Salom, {html.escape(message.from_user.full_name)}! O'yin boshlash uchun /game buyrug'ini yuboring.",
            parse_mode="HTML"
        )
        return

    # Lichkada: deep-linking tekshiruvi (/start num_gameid)
    args = message.text.split(maxsplit=1)
    if len(args) > 1 and args[1].startswith("num_"):
        game_id = args[1].replace("num_", "")
        game = games_manager.get_game(game_id)
        if game and game.game_type == "guess_number" and game.is_participant(message.from_user.id):
            if message.from_user.id in game.secret_numbers:
                await message.answer(
                    f"Siz allaqachon maxfiy soningizni tanlagansiz: <b>{game.secret_numbers[message.from_user.id]}</b>\n"
                    f"Guruhga qaytib o'yinni davom ettiring!",
                    parse_mode="HTML"
                )
            else:
                await message.answer(
                    "🔢 <b>Son Topish (1-100) O'yini:</b>\n\n"
                    "Iltimos, 1 dan 100 gacha bo'lgan maxfiy soningizni yozib yuboring (masalan: <code>42</code>):",
                    parse_mode="HTML"
                )
            return

    await message.answer(START_TEXT, parse_mode="HTML")


@common_router.message(F.chat.type == "private", F.text.regexp(r"^\s*(\d{1,3})\s*$"))
async def pm_set_secret_number(message: Message, bot: Bot):
    """Lichkada son topish uchun maxfiy sonni qabul qilish"""
    try:
        val = int(message.text.strip())
    except ValueError:
        return

    if not (1 <= val <= 100):
        await message.answer("Iltimos, faqat 1 dan 100 gacha oraliqda son kiriting!")
        return

    game = games_manager.find_user_waiting_guess_game(message.from_user.id)
    if not game:
        return

    game.secret_numbers[message.from_user.id] = val
    await message.answer(
        f"✅ Sizning maxfiy soningiz <b>{val}</b> sifatida saqlandi!\n\n"
        f"Guruhga qayting va o'yinni davom ettiring! 🚀",
        parse_mode="HTML"
    )

    # Agar ikkala o'yinchi ham sonini tanlab bo'lgan bo'lsa
    if len(game.secret_numbers) == 2:
        game.status = "playing"
        game.current_turn_id = game.initiator_id
        game.guess_bounds[game.initiator_id] = [1, 100]
        game.guess_bounds[game.opponent_id] = [1, 100]

        init_name = html.escape(game.initiator_name)
        opp_name = html.escape(game.opponent_name or "Raqib")

        try:
            start_msg = await bot.send_message(
                chat_id=game.chat_id,
                text=(
                    f"🔢 <b>Son Topish (1-100) Boshlandi!</b>\n\n"
                    f"👤 <b>{init_name}</b> ⚔️ 👤 <b>{opp_name}</b>\n\n"
                    f"✅ Har ikkala ishtirokchi ham o'z maxfiy sonini yashirdi!\n\n"
                    f"🎯 Har bir o'yinchi navbati kelganda raqib o'ylagan sonni guruh chatiga yozadi (masalan: <code>50</code>).\n"
                    f"Bot 'Kattaroq 📈' yoki 'Kichikroq 📉' deb ishora beradi.\n\n"
                    f"👉 1-navbat: <b>{init_name}</b>!\n"
                    f"Guruhga 1 dan 100 gacha bo'lgan taxminingizni yozing 👇"
                ),
                parse_mode="HTML"
            )
            schedule_delete_message(bot, game.chat_id, start_msg.message_id, GAME_MSG_DELETE_DELAY)
        except Exception:
            pass


@common_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(HELP_TEXT, parse_mode="HTML")

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
