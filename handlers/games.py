import html
import asyncio
from typing import Optional
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from games_manager import games_manager, GameSession
from penalties import get_random_penalty
from keyboards import (
    get_accept_challenge_keyboard,
    get_rps_keyboard,
    get_dice_roll_keyboard,
    get_rematch_keyboard,
    get_games_menu_keyboard
)

games_router = Router()

GAME_TITLES = {
    "rps": "🪨✂️📄 Tosh-Qaychi-Qog'oz",
    "dice": "🎲 Zar dueli",
    "darts": "🎯 Darts (Nishon)",
    "basket": "🏀 Basketbol",
    "football": "⚽ Futbol"
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
        f"⚠️ <i>Eslatma: Mag'lub bo'lgan ishtirokchini qiziqarli jazo kutmoqda!</i>\n"
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
    target_id = int(parts[2]) if len(parts) > 2 and parts[2] != "0" else None
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
            f"Tanlovingizni quyidagi tugmalardan birini bosib qiling 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_rps_keyboard(game.game_id),
            parse_mode="HTML"
        )
    else:
        # Zar / Emoji duel
        game.current_roller_id = game.initiator_id
        text = (
            f"🎮 <b>{game_title} Boshlandi!</b>\n\n"
            f"👤 <b>{init_name_safe}</b> ⚔️ 👤 <b>{opp_name_safe}</b>\n\n"
            f"🎲 Qoida: Har bir ishtirokchi navbat bilan {game.dice_emoji} tashlaydi. Eng yuqori ball to'plagan yutadi!\n\n"
            f"👉 1-navbat: <b>{init_name_safe}</b>!\n"
            f"Quyidagi tugmani bosing va zar tashlang 👇"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.initiator_name),
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
            f"Ikkala ishtirokchi ham tanlov qilsin 👇"
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
            f"Ikkalangiz ham bir xil tanladingiz! Qaytadan tanlang 👇"
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

        penalty = get_random_penalty()
        games_manager.remove_game(game.game_id)

        result_text = (
            f"🏆 <b>O'YIN YAKUNLANDI!</b>\n\n"
            f"👤 <b>{init_name_safe}</b>: {init_choice_str}\n"
            f"👤 <b>{opp_name_safe}</b>: {opp_choice_str}\n\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥇 <b>G'OLIB:</b> <b>{winner_name}</b> ({winner_choice}) 🎉\n"
            f"💀 <b>MAG'LUB:</b> <b>{loser_name}</b> ({loser_choice})\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"⚡️ <b>YUTQAZGAN UCHUN JAZO / TOPSHIRIQ:</b>\n"
            f"{penalty}\n\n"
            f"😜 <i>Mag'lub ishtirokchi shartni zudlik bilan guruhda bajarishi lozim!</i>"
        )

        await callback.message.edit_text(
            result_text,
            reply_markup=get_rematch_keyboard("rps"),
            parse_mode="HTML"
        )


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

    # Telegram animatsiyali zarni chatga jo'natish
    dice_msg = await bot.send_dice(chat_id=game.chat_id, emoji=game.dice_emoji)
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
            f"Quyidagi tugmani bosing va o'z zar/to'pingizni tashlang 👇"
        )
        await callback.message.answer(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.opponent_name or "Raqib"),
            parse_mode="HTML"
        )
        return

    # Ikkala ishtirokchi ham tashladi -> Taqqoslash!
    init_score = game.scores[game.initiator_id]
    opp_score = game.scores[game.opponent_id]

    if init_score == opp_score:
        # Durang
        game.scores.clear()
        game.current_roller_id = game.initiator_id
        text = (
            f"🤝 <b>DURANG BO'LDI!</b> ({init_score} - {opp_score})\n\n"
            f"Ikkala ishtirokchi ham bir xil natija ko'rsatdi!\n"
            f"Qaytadan tashlanadi. 1-navbat: <b>{init_name_safe}</b> 👇"
        )
        await callback.message.answer(
            text,
            reply_markup=get_dice_roll_keyboard(game.game_id, game.dice_emoji, game.initiator_name),
            parse_mode="HTML"
        )
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

        penalty = get_random_penalty()
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
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"⚡️ <b>YUTQAZGAN UCHUN JAZO / TOPSHIRIQ:</b>\n"
            f"{penalty}\n\n"
            f"😜 <i>Mag'lub bo'lgan ishtirokchi shartni guruhda bajarishi shart!</i>"
        )

        await callback.message.answer(
            result_text,
            reply_markup=get_rematch_keyboard(game_type),
            parse_mode="HTML"
        )


# ---- QAYTA O'YNASH (REMATCH) ----

@games_router.callback_query(F.data.startswith("rematch:"))
async def cb_rematch(callback: CallbackQuery):
    game_type = callback.data.split(":")[1]
    await initiate_game(callback.message, game_type, initiator=callback.from_user)
    await callback.answer("Yangi duel chaqiruvi yuborildi! 🚀")
