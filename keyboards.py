from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_games_menu_keyboard(target_user_id: int = 0, opener_user_id: int = 0) -> InlineKeyboardMarkup:
    """O'yin turini tanlash menyusi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🪨✂️📄 Tosh-Qaychi-Qog'oz",
                    callback_data=f"start_type:rps:{target_user_id}:{opener_user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎲 Zar dueli",
                    callback_data=f"start_type:dice:{target_user_id}:{opener_user_id}"
                ),
                InlineKeyboardButton(
                    text="🎯 Darts (Nishon)",
                    callback_data=f"start_type:darts:{target_user_id}:{opener_user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏀 Basketbol dueli",
                    callback_data=f"start_type:basket:{target_user_id}:{opener_user_id}"
                ),
                InlineKeyboardButton(
                    text="⚽ Futbol penalti",
                    callback_data=f"start_type:football:{target_user_id}:{opener_user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Yopish",
                    callback_data=f"close_menu:{opener_user_id}"
                )
            ]
        ]
    )

def get_accept_challenge_keyboard(game_id: str) -> InlineKeyboardMarkup:
    """Duelga chaqiruvni qabul qilish tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚔️ Duelni qabul qilish!",
                    callback_data=f"accept:{game_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"cancel:{game_id}"
                )
            ]
        ]
    )

def get_rps_keyboard(game_id: str) -> InlineKeyboardMarkup:
    """Tosh-Qaychi-Qog'oz tanlov tugmalari"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🪨 Tosh", callback_data=f"rps:{game_id}:rock"),
                InlineKeyboardButton(text="✂️ Qaychi", callback_data=f"rps:{game_id}:scissors"),
                InlineKeyboardButton(text="📄 Qog'oz", callback_data=f"rps:{game_id}:paper"),
            ]
        ]
    )

def get_dice_roll_keyboard(game_id: str, emoji: str, roller_name: str) -> InlineKeyboardMarkup:
    """Zar yoki emoji tashlash tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{emoji} {roller_name} tashlaydi!",
                    callback_data=f"roll:{game_id}"
                )
            ]
        ]
    )

def get_rematch_keyboard(game_type: str) -> InlineKeyboardMarkup:
    """O'yin tugagandan keyin qayta o'ynash tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Yangi duel boshlash",
                    callback_data=f"rematch:{game_type}"
                )
            ]
        ]
    )
