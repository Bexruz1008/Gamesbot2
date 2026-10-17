import html
import asyncio
import random
from typing import Optional
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from games_manager import games_manager, GameSession
from keyboards import (
    get_accept_challenge_keyboard,
    get_rps_keyboard,
    get_dice_roll_keyboard,
    get_rematch_keyboard,
    get_games_menu_keyboard,
    get_roulette_keyboard,
    get_ttt_keyboard,
    get_guess_number_setup_keyboard
)

# Xabarlarni avtomatik o'chirish muddatlari (soniyalarda)
GAME_MSG_DELETE_DELAY = 5 * 60         # 5 daqiqa (zar, darts va oraliq xabarlar)
FINAL_RESULT_DELETE_DELAY = 1 * 3600   # 1 soat (g'olib e'lon qilingan natija xabari)

def schedule_delete_message(bot: Bot, chat_id: int, message_id: int, delay_seconds: int):
    """Xabarni orqa fonda belgilangan muddatdan so'ng xavfsiz o'chirish"""
    async def _delete():
        try:
            await asyncio.sleep(delay_seconds)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
    asyncio.create_task(_delete())


games_router = Router()

GAME_TITLES = {
    "rps": "🪨✂️📄 Tosh-Qaychi-Qog'oz",
    "dice": "🎲 Zar dueli",
    "darts": "🎯 Darts (Nishon)",
    "basket": "🏀 Basketbol",
    "football": "⚽ Futbol",
    "bowling": "🎳 Bowling",
    "roulette": "💣 Rus Ruletkasi",
    "tictactoe": "❌⭕ Tic-Tac-Toe",
    "guess_number": "🔢 Son Topish (1-100)"
}

RPS_NAMES = {
    "rock": "🪨 Tosh",
    "scissors": "✂️ Qaychi",
    "paper": "📄 Qog'oz"
}

def determine_rps_winner(c1: str, c2: str) -> int:
    """
    1 agar c1 yutsa, 2 agar c2 yutsa, 0 agar durang bo'lsa
    """
    if c1 == c2:
        return 0
    wins = {
        ("rock", "scissors"): True,
        ("scissors", "paper"): True,
        ("paper", "rock"): True
    }
    return 1 if (c1, c2) in wins else 2

async def initiate_game(
    message: Message,
    game_type: str,
    target_id: Optional[int] = None,
    target_name: Optional[str] = None,
    initiator=None
):
    """Yangi o'yin dueli xabarini yaratish va guruhga jo'natish"""
    initiator = initiator or message.from_user
    chat_id = message.chat.id

    game = games_manager.create_game(
        chat_id=chat_id,
        game_type=game_type,
        initiator_id=initiator.id,
        initiator_name=initiator.full_name,
        opponent_id=target_id,
        opponent_name=target_name
    )

    init_name_safe = html.escape(initiator.full_name)
    game_title = GAME_TITLES.get(game_type, "Mini o'yin")

    if target_id and target_name:
        opp_text = f"<b>{html.escape(target_name)}</b>"
    else:
        opp_text = "<i>Har qanday xohlovchi</i>"

    text = (
        f"⚔️ <b>DUEL CHAQIRUVI!</b>\n\n"
        f"🎮 <b>O'yin:</b> {game_title}\n"
        f"👤 <b>Tashabbuskor:</b> <b>{init_name_safe}</b>\n"
        f"🎯 <b>Raqib:</b> {opp_text}\n\n"
        f"Duelni qabul qilish uchun quyidagi tugmani bosing 👇"
    )

    sent_msg = await message.answer(
        text,
        reply_markup=get_accept_challenge_keyboard(game.game_id),
        parse_mode="HTML"
    )
    game.message_id = sent_msg.message_id


# ---- BUYRUQLAR (COMMANDS) ----

@games_router.message(Command("rps", "tosh"))
async def cmd_rps(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "rps", target_id, target_name)

@games_router.message(Command("dice", "zar"))
async def cmd_dice(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "dice", target_id, target_name)

@games_router.message(Command("darts", "nishon"))
async def cmd_darts(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "darts", target_id, target_name)

@games_router.message(Command("basket"))
async def cmd_basket(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "basket", target_id, target_name)

@games_router.message(Command("football", "futbol"))
async def cmd_football(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "football", target_id, target_name)

@games_router.message(Command("bowling", "bouling"))
async def cmd_bowling(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "bowling", target_id, target_name)

@games_router.message(Command("roulette", "ruletka"))
async def cmd_roulette(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "roulette", target_id, target_name)

@games_router.message(Command("tictactoe", "xo"))
async def cmd_tictactoe(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "tictactoe", target_id, target_name)

@games_router.message(Command("guess", "sontop"))
async def cmd_guess(message: Message):
    target_id, target_name = _extract_target(message)
    await initiate_game(message, "guess_number", target_id, target_name)

@games_router.message(Command("duel"))
async def cmd_duel(message: Message):
    # Agar reply qilingan bo'lsa o'sha user bilan menyu ochadi
    target_id, target_name = _extract_target(message)
    init_name_safe = html.escape(message.from_user.full_name)
    if target_id and target_name:
        text = f"⚔️ <b>{init_name_safe}</b> vs <b>{html.escape(target_name)}</b>!\nQaysi o'yinni tanlaysiz?"
    else:
        text = f"⚔️ <b>{init_name_safe}</b> duel boshlamoqchi!\nQaysi o'yinni tanlaysiz?"

    await message.reply(
        text,
        reply_markup=get_games_menu_keyboard(target_id or 0, message.from_user.id),
        parse_mode="HTML"
    )

def _extract_target(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        target = message.reply_to_message.from_user
        if not target.is_bot and target.id != message.from_user.id:
            return target.id, target.full_name
    return None, None


# ---- CALLBACK QUERY HANDLERS ----

@games_router.callback_query(F.data.startswith("start_type:"))
async def cb_start_type(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) != 4:
        await callback.answer("Bu menyu eskirgan. Yangi /game buyrug'ini yuboring.", show_alert=True)
        return

    game_type = parts[1]
    target_id = int(parts[2]) if parts[2] != "0" else None
    opener_id = int(parts[3])
    if callback.from_user.id != opener_id:
        await callback.answer("O'yin turini faqat menyuni ochgan odam tanlay oladi.", show_alert=True)
        return
    target_name = None

    # Eski xabarni o'chirib yangi chaqiruv chiqarish
    try:
        await callback.message.delete()
    except Exception:
        pass

    await initiate_game(callback.message, game_type, target_id, target_name, callback.from_user)
    await callback.answer()


@games_router.callback_query(F.data.startswith("accept:"))
async def cb_accept_game(callback: CallbackQuery, bot: Bot):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game:
        await callback.answer("Bu o'yin allaqachon tugagan yoki mavjud emas!", show_alert=True)
        return

    user = callback.from_user

    # Tashabbuskor o'zi bilan o'zi o'ynay olmaydi
    if user.id == game.initiator_id:
        await callback.answer("O'z chaqiruvingizni qabul qila olmaysiz! Boshqa ishtirokchini kuting.", show_alert=True)
        return

    # Agar aniq bitta odamga yuborilgan bo'lsa
    if game.opponent_id and user.id != game.opponent_id:
        await callback.answer("Bu chaqiruv siz uchun emas!", show_alert=True)
        return

    # Raqibni biriktiramiz
    game.opponent_id = user.id
    game.opponent_name = user.full_name
    # guess_number uchun status setting_numbers ga pastda o'rnatiladi
    if game.game_type != "guess_number":
        game.status = "playing"

    init_name_safe = html.escape(game.initiator_name)
    opp_name_safe = html.escape(game.opponent_name)
    game_title = GAME_TITLES.get(game.game_type, "Mini o'yin")

    await callback.answer("Duel qabul qilindi! O'yin boshlandi! 🔥")

    if game.game_type == "rps":
        text = (
            f"🎮 <b>{game_title} Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"Ikkala ishtirokchi ham o'z tanlovini qilsin (tanlov maxfiy qoladi):\n"
            f"• <b>{init_name_safe}</b>: ⏳ Kutilyapti\n"
            f"• <b>{opp_name_safe}</b>: ⏳ Kutilyapti\n\n"
            f"O'z tanlovingizni qiling 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_rps_keyboard(game.game_id),
            parse_mode="HTML"
        )
    elif game.game_type in ("dice", "darts", "basket", "football", "bowling"):
        # Zar / Emoji duel
        game.current_roller_id = game.initiator_id
        text = (
            f"🎮 <b>{game_title} Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"🎲 Qoida: Har bir ishtirokchi navbat bilan {game.dice_emoji} tashlaydi. Eng yuqori ball to'plagan yutadi!\n\n"
            f"👉 1-navbat: <b>{init_name_safe}</b>!\n"
            f"Quyidagi tugmani bosib o'z natijangizni tashlang 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.initiator_name),
            parse_mode="HTML"
        )
    elif game.game_type == "roulette":
        # Rus Ruletkasi
        game.current_turn_id = game.initiator_id
        text = (
            f"💣 <b>Rus Ruletkasi Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"🔫 Barabanda 6 ta patron joyi mavjud, ulardan 1 tasida patron bor.\n"
            f"Navbatma-navbat tepkini bosasiz. Kimda patron chiqsa — o'sha mag'lub!\n\n"
            f"🔄 Patron joyi: <b>1 / 6</b>\n"
            f"👉 1-navbat: <b>{init_name_safe}</b>!\n"
            f"Tepkini bosing 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_roulette_keyboard(game.game_id, game.initiator_name),
            parse_mode="HTML"
        )
    elif game.game_type == "tictactoe":
        # Tic-Tac-Toe
        game.ttt_symbols = {game.initiator_id: "❌", game.opponent_id: "⭕"}
        game.current_turn_id = game.initiator_id
        text = (
            f"❌⭕ <b>Tic-Tac-Toe Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> (❌) ⚔️ 👤 <b>{opp_name_safe}</b> (⭕)\n\n"
            f"👉 1-navbat: <b>{init_name_safe}</b> (❌)\n"
            f"Bo'sh kataklardan birini tanlang 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_ttt_keyboard(game.game_id, game.ttt_board),
            parse_mode="HTML"
        )
    elif game.game_type == "guess_number":
        # Son topish
        game.status = "setting_numbers"
        bot_info = await bot.get_me()
        bot_username = bot_info.username or ""
        text = (
            f"🔢 <b>Son Topish (1-100) Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"1️⃣ Ikkala ishtirokchi ham o'z maxfiy sonini tanlashi lozim:\n"
            f"• <b>{init_name_safe}</b>: ⏳ Tanlanmadi\n"
            f"• <b>{opp_name_safe}</b>: ⏳ Tanlanmadi\n\n"
            f"Quyidagi tugmalar orqali tasodifiy son oling yoki bot lichkasida o'z soningizni yashiring 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_guess_number_setup_keyboard(game.game_id, bot_username),
            parse_mode="HTML"
        )


@games_router.callback_query(F.data.startswith("cancel:"))
async def cb_cancel_game(callback: CallbackQuery):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game:
        await callback.answer("O'yin allaqachon bekor qilingan.", show_alert=True)
        return

    # Faqat tashabbuskor bekor qila oladi
    if callback.from_user.id != game.initiator_id:
        await callback.answer("Faqat o'yin tashabbuskori uni bekor qilishi mumkin!", show_alert=True)
        return

    games_manager.remove_game(game_id)
    await callback.message.edit_text(
        f"❌ <b>{html.escape(game.initiator_name)}</b> duel chaqiruvini bekor qildi.",
        parse_mode="HTML"
    )
    await callback.answer("Bekor qilindi.")


# ---- TOSH-QAYCHI-QOG'OZ HANDLERS ----

@games_router.callback_query(F.data.startswith("rps:"))
async def cb_rps_choice(callback: CallbackQuery):
    parts = callback.data.split(":")
    game_id = parts[1]
    choice = parts[2]

    game = games_manager.get_game(game_id)
    if not game or game.status != "playing":
        await callback.answer("O'yin yakunlangan yoki topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu o'yinda qatnashmayapsiz! Yangi duel boshlashingiz mumkin.", show_alert=True)
        return

    if user_id in game.rps_choices:
        await callback.answer("Siz allaqachon tanlovingizni qilgansiz! Raqibingizni kuting.", show_alert=True)
        return

    # Tanlovni saqlash
    game.rps_choices[user_id] = choice
    choice_name = RPS_NAMES.get(choice, choice)
    await callback.answer(f"Siz {choice_name} tanladingiz! Tanlov saqlandi. ✅", show_alert=False)

    init_name_safe = html.escape(game.initiator_name)
    opp_name_safe = html.escape(game.opponent_name or "Raqib")
    game_title = GAME_TITLES.get(game.game_type, "Tosh-Qaychi-Qog'oz")

    # Agar hali ikkinchi odam tanlamagan bo'lsa
    if len(game.rps_choices) < 2:
        init_status = "✅ Tanladi" if game.initiator_id in game.rps_choices else "⏳ Kutilyapti"
        opp_status = "✅ Tanladi" if game.opponent_id in game.rps_choices else "⏳ Kutilyapti"

        text = (
            f"🎮 <b>{game_title} Bormoqda!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"• <b>{init_name_safe}</b>: {init_status}\n"
            f"• <b>{opp_name_safe}</b>: {opp_status}\n\n"
            f"Ikkala ishtirokchi ham o'z tanlovini qilsin 👇"
        )
        try:
            await callback.message.edit_text(
                text,
                reply_markup=get_rps_keyboard(game.game_id),
                parse_mode="HTML"
            )
        except Exception:
            pass
        return

    # Ikkala ishtirokchi ham tanladi -> Natijani hisoblash!
    init_choice = game.rps_choices[game.initiator_id]
    opp_choice = game.rps_choices[game.opponent_id]

    init_choice_str = RPS_NAMES.get(init_choice, init_choice)
    opp_choice_str = RPS_NAMES.get(opp_choice, opp_choice)

    res = determine_rps_winner(init_choice, opp_choice)

    if res == 0:
        # Durang!
        game.rps_choices.clear()
        text = (
            f"🤝 <b>DURANG BO'LDI!</b>\n\n"
            f"👤 <b>{init_name_safe}</b>: {init_choice_str}\n"
            f"👤 <b>{opp_name_safe}</b>: {opp_choice_str}\n\n"
            f"Ikki tomondan ham bir xil tanlov! Qaytadan tanlang 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_rps_keyboard(game.game_id),
            parse_mode="HTML"
        )
    else:
        # G'olib aniqlandi
        if res == 1:
            winner_name = init_name_safe
            winner_choice = init_choice_str
            loser_name = opp_name_safe
            loser_choice = opp_choice_str
        else:
            winner_name = opp_name_safe
            winner_choice = opp_choice_str
            loser_name = init_name_safe
            loser_choice = init_choice_str

        games_manager.remove_game(game.game_id)

        result_text = (
            f"🏆 <b>O'YIN YAKUNLANDI!</b>\n\n"
            f"👤 <b>{init_name_safe}</b>: {init_choice_str}\n"
            f"👤 <b>{opp_name_safe}</b>: {opp_choice_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> ({winner_choice}) 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b> ({loser_choice})\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        await callback.message.edit_text(
            result_text,
            reply_markup=get_rematch_keyboard("rps"),
            parse_mode="HTML"
        )
        if callback.bot and callback.message:
            schedule_delete_message(callback.bot, callback.message.chat.id, callback.message.message_id, FINAL_RESULT_DELETE_DELAY)


# ---- ZAR / EMOJI DUELI HANDLERS ----

@games_router.callback_query(F.data.startswith("roll:"))
async def cb_dice_roll(callback: CallbackQuery, bot: Bot):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game or game.status != "playing":
        await callback.answer("O'yin yakunlangan yoki topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu duelda qatnashmayapsiz!", show_alert=True)
        return

    if user_id != game.current_roller_id:
        await callback.answer("Hozir sizning navbatingiz emas! Raqibingizni kuting.", show_alert=True)
        return

    await callback.answer(f"{game.dice_emoji} Tashlanmoqda...")

    init_name_safe = html.escape(game.initiator_name)
    opp_name_safe = html.escape(game.opponent_name or "Raqib")
    user_name_safe = html.escape(callback.from_user.full_name)

    # Race condition oldini olish: navbatni darhol tozalaymiz
    # (send_dice async kutish paytida ikkinchi marta bosilmasin)
    game.current_roller_id = None

    # Telegram animatsiyali zarni chatga jo'natish
    dice_msg = await bot.send_dice(chat_id=game.chat_id, emoji=game.dice_emoji)
    # Tashlangan tosh/dart/zar 5 daqiqadan so'ng avtomatik o'chadi
    schedule_delete_message(bot, game.chat_id, dice_msg.message_id, GAME_MSG_DELETE_DELAY)

    score = dice_msg.dice.value
    game.scores[user_id] = score

    # Animatsiya to'liq ko'rinishi uchun biroz kutish (3.5 soniya)
    await asyncio.sleep(3.5)

    # 1-ishtirokchi tashlagan bo'lsa
    if len(game.scores) == 1:
        game.current_roller_id = game.opponent_id
        text = (
            f"🎲 <b>{game.dice_emoji} {GAME_TITLES.get(game.game_type, 'Duel')}</b>\n\n"
            f"👤 <b>{user_name_safe}</b> natijasi: <b>{score}</b> ball! {game.dice_emoji}\n\n"
            f"👉 Endi navbat: <b>{opp_name_safe}</b>!\n"
            f"Quyidagi tugmani bosib o'z natijangizni tashlang 👇"
        )
        turn_msg = await callback.message.answer(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.opponent_name or "Raqib"),
            parse_mode="HTML"
        )
        # Oraliq o'yin xabari 5 daqiqadan so'ng o'chadi
        schedule_delete_message(bot, game.chat_id, turn_msg.message_id, GAME_MSG_DELETE_DELAY)
        # Oldingi navbat tugmasi xabarini ham 5 daqiqada o'chirishga qo'yish
        if callback.message:
            schedule_delete_message(bot, game.chat_id, callback.message.message_id, GAME_MSG_DELETE_DELAY)
        return

    # Ikkala ishtirokchi ham tashladi -> Taqqoslash!
    init_score = game.scores[game.initiator_id]
    opp_score = game.scores[game.opponent_id]

    if init_score == opp_score:
        # Durang
        game.scores.clear()
        game.current_roller_id = game.initiator_id
        text = (
            f"🤝 <b>DURANG BO'LDI!</b> ({init_score} — {opp_score})\n\n"
            f"Ikkala ishtirokchi ham bir xil natija ko'rsatdi!\n"
            f"Qaytadan tashlanadi. 1-navbat: <b>{init_name_safe}</b> 👇"
        )
        draw_msg = await callback.message.answer(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.initiator_name),
            parse_mode="HTML"
        )
        schedule_delete_message(bot, game.chat_id, draw_msg.message_id, GAME_MSG_DELETE_DELAY)
        if callback.message:
            schedule_delete_message(bot, game.chat_id, callback.message.message_id, GAME_MSG_DELETE_DELAY)
    else:
        # G'olib aniqlandi
        if init_score > opp_score:
            winner_name = init_name_safe
            winner_score = init_score
            loser_name = opp_name_safe
            loser_score = opp_score
        else:
            winner_name = opp_name_safe
            winner_score = opp_score
            loser_name = init_name_safe
            loser_score = init_score

        game_type = game.game_type
        dice_emoji = game.dice_emoji
        games_manager.remove_game(game.game_id)

        result_text = (
            f"🏁 <b>DUEL YAKUNLANDI!</b> {dice_emoji}\n\n"
            f"👤 <b>{init_name_safe}</b>: {init_score} ball\n"
            f"👤 <b>{opp_name_safe}</b>: {opp_score} ball\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> ({winner_score} ball) 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b> ({loser_score} ball)\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        final_msg = await callback.message.answer(
            result_text,
            reply_markup=get_rematch_keyboard(game_type),
            parse_mode="HTML"
        )
        # G'olib nomi e'lon qilingan natija xabari 12 soatdan so'ng o'chadi
        schedule_delete_message(bot, game.chat_id, final_msg.message_id, FINAL_RESULT_DELETE_DELAY)
        # Oldingi navbat xabari esa 5 daqiqada o'chadi
        if callback.message:
            schedule_delete_message(bot, game.chat_id, callback.message.message_id, GAME_MSG_DELETE_DELAY)


# ---- QAYTA O'YNASH (REMATCH) ----

@games_router.callback_query(F.data.startswith("rematch:"))
async def cb_rematch(callback: CallbackQuery):
    game_type = callback.data.split(":")[1]
    await initiate_game(callback.message, game_type, initiator=callback.from_user)
    await callback.answer("Yangi duel chaqiruvi yuborildi! 🚀")


# ---- RUS RULETKASI HANDLERS ----

@games_router.callback_query(F.data.startswith("trigger:"))
async def cb_roulette_trigger(callback: CallbackQuery, bot: Bot):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game or game.status != "playing":
        await callback.answer("O'yin yakunlangan yoki topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu duelda qatnashmayapsiz!", show_alert=True)
        return

    if user_id != game.current_turn_id:
        await callback.answer("Hozir sizning navbatingiz emas! Raqibingizni kuting.", show_alert=True)
        return

    game.roulette_chamber += 1

    # Tekshiramiz: patron chiqdimi?
    if game.roulette_chamber - 1 == game.roulette_bullet:
        # BOOM! Patron otildi!
        other_id = game.get_other_user_id(user_id)
        winner_name = html.escape(game.get_user_name(other_id))
        loser_name = html.escape(callback.from_user.full_name)

        games_manager.remove_game(game.game_id)

        result_text = (
            f"💥 <b>BOOM! O'Q OTILDI!</b> 💣\n\n"
            f"💀 <b>{loser_name}</b> ning navbatida o'q chiqdi! Omadsiz...\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        await callback.message.edit_text(
            result_text,
            reply_markup=get_rematch_keyboard("roulette"),
            parse_mode="HTML"
        )
        schedule_delete_message(bot, game.chat_id, callback.message.message_id, FINAL_RESULT_DELETE_DELAY)
        await callback.answer("💥 O'q otildi!", show_alert=True)
    else:
        # Omadli o'tdi (Click!)
        other_id = game.get_other_user_id(user_id)
        game.current_turn_id = other_id
        other_name = html.escape(game.get_user_name(other_id))
        current_name = html.escape(callback.from_user.full_name)

        text = (
            f"💣 <b>Rus Ruletkasi Davom Etmoqda!</b>\n\n"
            f"🔫 <b>*CLICK!*</b> Bo'sh patron joyi! <b>{current_name}</b> omon qoldi! 😅\n\n"
            f"🔄 Keyingi patron joyi: <b>{game.roulette_chamber + 1} / 6</b>\n"
            f"👉 Navbat: <b>{other_name}</b>!\n\n"
            f"Tepkini bosing 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_roulette_keyboard(game.game_id, other_name),
            parse_mode="HTML"
        )
        await callback.answer("Click! Patron joyi bo'sh! Omad keldi.")


# ---- TIC-TAC-TOE HANDLERS ----

@games_router.callback_query(F.data.startswith("ttt:"))
async def cb_ttt_move(callback: CallbackQuery, bot: Bot):
    parts = callback.data.split(":")
    game_id = parts[1]
    cell_idx = int(parts[2])

    game = games_manager.get_game(game_id)
    if not game or game.status != "playing":
        await callback.answer("O'yin yakunlangan yoki topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu duelda qatnashmayapsiz!", show_alert=True)
        return

    if user_id != game.current_turn_id:
        await callback.answer("Hozir sizning navbatingiz emas! Raqibingizni kuting.", show_alert=True)
        return

    if game.ttt_board[cell_idx] != "⬜":
        await callback.answer("Bu katak allaqachon band!", show_alert=True)
        return

    my_symbol = game.ttt_symbols.get(user_id, "❌")
    game.ttt_board[cell_idx] = my_symbol

    win_result = game.check_ttt_winner()

    if win_result in ("❌", "⭕"):
        # G'olib aniqlandi
        other_id = game.get_other_user_id(user_id)
        winner_name = html.escape(callback.from_user.full_name)
        loser_name = html.escape(game.get_user_name(other_id))

        games_manager.remove_game(game.game_id)

        result_text = (
            f"🏁 <b>TIC-TAC-TOE YAKUNLANDI!</b> ❌⭕\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> ({win_result}) 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        await callback.message.edit_text(
            result_text,
            reply_markup=get_rematch_keyboard("tictactoe"),
            parse_mode="HTML"
        )
        schedule_delete_message(bot, game.chat_id, callback.message.message_id, FINAL_RESULT_DELETE_DELAY)
        await callback.answer("G'olib bo'ldingiz! 🎉")

    elif win_result == "draw":
        # Durang
        games_manager.remove_game(game.game_id)
        result_text = (
            f"🤝 <b>DURANG BO'LDI!</b> ❌⭕\n\n"
            f"Barcha 9 ta katak to'ldi, g'olib aniqlanmadi!\n"
        )
        await callback.message.edit_text(
            result_text,
            reply_markup=get_rematch_keyboard("tictactoe"),
            parse_mode="HTML"
        )
        schedule_delete_message(bot, game.chat_id, callback.message.message_id, GAME_MSG_DELETE_DELAY)
        await callback.answer("Durang!")

    else:
        # O'yin davom etmoqda
        other_id = game.get_other_user_id(user_id)
        game.current_turn_id = other_id
        other_name = html.escape(game.get_user_name(other_id))
        other_symbol = game.ttt_symbols.get(other_id, "⭕")

        text = (
            f"❌⭕ <b>Tic-Tac-Toe Davom Etmoqda!</b>\n\n"
            f"👤 <b>{html.escape(game.initiator_name)}</b> (❌) ⚔️ 👤 <b>{html.escape(game.opponent_name or 'Raqib')}</b> (⭕)\n\n"
            f"👉 Navbat: <b>{other_name}</b> ({other_symbol}) 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_ttt_keyboard(game.game_id, game.ttt_board),
            parse_mode="HTML"
        )
        await callback.answer()


# ---- TASLIM BO'LISH (SURRENDER) ----

@games_router.callback_query(F.data.startswith("surrender:"))
async def cb_surrender(callback: CallbackQuery, bot: Bot):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game or game.status != "playing":
        await callback.answer("O'yin topilmadi yoki yakunlangan.", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu duelda qatnashmayapsiz!", show_alert=True)
        return

    other_id = game.get_other_user_id(user_id)
    winner_name = html.escape(game.get_user_name(other_id))
    loser_name = html.escape(callback.from_user.full_name)
    game_type = game.game_type

    games_manager.remove_game(game.game_id)

    result_text = (
        f"🏳️ <b>TASLIM BO'LINDI!</b>\n\n"
        f"👤 <b>{loser_name}</b> o'z xohishi bilan taslim bo'ldi!\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> 🏆\n"
        f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    await callback.message.edit_text(
        result_text,
        reply_markup=get_rematch_keyboard(game_type),
        parse_mode="HTML"
    )
    schedule_delete_message(bot, game.chat_id, callback.message.message_id, FINAL_RESULT_DELETE_DELAY)
    await callback.answer("Taslim bo'ldingiz.")


# ---- SON TOPISH (1-100) HANDLERS ----

@games_router.callback_query(F.data.startswith("rndnum:"))
async def cb_random_number(callback: CallbackQuery, bot: Bot):
    game_id = callback.data.split(":")[1]
    game = games_manager.get_game(game_id)

    if not game or game.game_type != "guess_number":
        await callback.answer("O'yin topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    if not game.is_participant(user_id):
        await callback.answer("Siz bu o'yinda qatnashmayapsiz!", show_alert=True)
        return

    if user_id in game.secret_numbers:
        await callback.answer(f"Sizning maxfiy soningiz: {game.secret_numbers[user_id]} (allaqachon belgilangan)", show_alert=True)
        return

    secret = random.randint(1, 100)
    game.secret_numbers[user_id] = secret
    await callback.answer(f"🤫 Sizning maxfiy soningiz: {secret}!\nUni eslab qoling va raqibga aytmang!", show_alert=True)

    init_id = game.initiator_id
    opp_id = game.opponent_id

    # Agar ikkala o'yinchi ham son tanlab bo'lsa
    if len(game.secret_numbers) == 2:
        game.status = "playing"
        game.current_turn_id = init_id
        game.guess_bounds[init_id] = [1, 100]
        game.guess_bounds[opp_id] = [1, 100]

        init_name = html.escape(game.initiator_name)
        opp_name = html.escape(game.opponent_name or "Raqib")

        text = (
            f"🔢 <b>Son Topish (1-100) Boshlandi!</b>\n\n"
            f"👤 <b>{init_name}</b> ⚔️ 👤 <b>{opp_name}</b>\n\n"
            f"✅ Har ikkala ishtirokchi ham o'z maxfiy sonini yashirdi!\n\n"
            f"🎯 Har bir o'yinchi navbatida raqib o'ylagan sonni guruh chatiga yozadi (masalan: <code>50</code>).\n"
            f"Bot '📈 Kattaroq' yoki '📉 Kichikroq' deb ishora beradi.\n\n"
            f"👉 1-navbat: <b>{init_name}</b>!\n"
            f"Guruhga 1 dan 100 gacha bo'lgan taxminingizni yozing 👇"
        )
        await callback.message.edit_text(text, parse_mode="HTML")
    else:
        # Hali 1 ta o'yinchi tanlashi kutilmoqda
        p1_status = "✅ Tanlandi" if init_id in game.secret_numbers else "⏳ Tanlanmadi"
        p2_status = "✅ Tanlandi" if opp_id in game.secret_numbers else "⏳ Tanlanmadi"
        bot_info = await bot.get_me()
        bot_username = bot_info.username or ""

        text = (
            f"🔢 <b>Son Topish (1-100) Boshlandi!</b>\n\n"
            f"👤 <b>{html.escape(game.initiator_name)}</b> ⚔️ 👤 <b>{html.escape(game.opponent_name or 'Raqib')}</b>\n\n"
            f"1️⃣ Ikkala ishtirokchi ham o'z maxfiy sonini tanlashi lozim:\n"
            f"• <b>{html.escape(game.initiator_name)}</b>: {p1_status}\n"
            f"• <b>{html.escape(game.opponent_name or 'Raqib')}</b>: {p2_status}\n\n"
            f"Quyidagi tugmalar orqali tasodifiy son oling yoki bot lichkasida o'z soningizni yashiring 👇"
        )
        try:
            await callback.message.edit_text(
                text,
                reply_markup=get_guess_number_setup_keyboard(game.game_id, bot_username),
                parse_mode="HTML"
            )
        except Exception:
            pass


@games_router.message(F.text.regexp(r"^\s*(\d{1,3})\s*$"))
async def handle_guess_number_message(message: Message, bot: Bot):
    """Guruhda son topish navbati kelgan ishtirokchi son yozganida tekshirish"""
    if message.chat.type not in ("group", "supergroup"):
        return

    try:
        guess_val = int(message.text.strip())
    except ValueError:
        return

    if not (1 <= guess_val <= 100):
        return

    game = games_manager.find_active_guess_game(message.chat.id, message.from_user.id)
    if not game:
        return

    other_id = game.get_other_user_id(message.from_user.id)
    if not other_id or other_id not in game.secret_numbers:
        return

    target_num = game.secret_numbers[other_id]
    user_name = html.escape(message.from_user.full_name)
    other_name = html.escape(game.get_user_name(other_id))

    # O'yinchining taxmin xabarini 5 daqiqadan so'ng o'chirish
    schedule_delete_message(bot, message.chat.id, message.message_id, GAME_MSG_DELETE_DELAY)

    if guess_val == target_num:
        # G'olib!
        games_manager.remove_game(game.game_id)
        result_text = (
            f"🎯 <b>TO'G'RI TOPILDI! DUEL YAKUNLANDI!</b> 🔢\n\n"
            f"👤 <b>{user_name}</b> raqibi o'ylagan <b>{target_num}</b> sonini topdi! 👏\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{user_name}</b> 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{other_name}</b>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        win_msg = await message.answer(
            result_text,
            reply_markup=get_rematch_keyboard("guess_number"),
            parse_mode="HTML"
        )
        schedule_delete_message(bot, message.chat.id, win_msg.message_id, FINAL_RESULT_DELETE_DELAY)
    else:
        # Noto'g'ri: Kattaroq yoki Kichikroq
        user_id = message.from_user.id
        # Mavjud chegaralarni olish (agar yo'q bo'lsa [1,100] bilan yaratish)
        if user_id not in game.guess_bounds:
            game.guess_bounds[user_id] = [1, 100]
        bounds = game.guess_bounds[user_id]

        if guess_val < target_num:
            direction = "📈 Raqibingiz o'ylagan son bundan <b>KATTAROQ!</b>"
            bounds[0] = max(bounds[0], guess_val + 1)
        else:
            direction = "📉 Raqibingiz o'ylagan son bundan <b>KICHIKROQ!</b>"
            bounds[1] = min(bounds[1], guess_val - 1)
        # bounds list reference bo'lganligi sababli o'zgarish avtomatik saqlanadi

        # Navbatni boshqasiga o'tkazish
        game.current_turn_id = other_id

        hint_text = (
            f"{direction}\n"
            f"👤 <b>{user_name}</b> taxmini: <b>{guess_val}</b> | Oraliq: {bounds[0]} — {bounds[1]}\n\n"
            f"👉 Endi navbat: <b>{other_name}</b>!\n"
            f"Taxminingizni guruhga yozing 👇"
        )
        hint_msg = await message.answer(hint_text, parse_mode="HTML")
        schedule_delete_message(bot, message.chat.id, hint_msg.message_id, GAME_MSG_DELETE_DELAY)

