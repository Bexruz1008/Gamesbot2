from typing import List
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
                    text="🎳 Bowling dueli",
                    callback_data=f"start_type:bowling:{target_user_id}:{opener_user_id}"
                ),
                InlineKeyboardButton(
                    text="💣 Rus Ruletkasi",
                    callback_data=f"start_type:roulette:{target_user_id}:{opener_user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌⭕ Tic-Tac-Toe",
                    callback_data=f"start_type:tictactoe:{target_user_id}:{opener_user_id}"
                ),
                InlineKeyboardButton(
                    text="🔢 Son Topish (1-100)",
                    callback_data=f"start_type:guess_number:{target_user_id}:{opener_user_id}"
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

def get_roulette_keyboard(game_id: str, player_name: str) -> InlineKeyboardMarkup:
    """Rus ruletkasida tepkini bosish tugmasi"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🔫 {player_name} tepkini bosadi!",
                    callback_data=f"trigger:{game_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏳️ Taslim bo'lish",
                    callback_data=f"surrender:{game_id}"
                )
            ]
        ]
    )

def get_ttt_keyboard(game_id: str, board: List[str]) -> InlineKeyboardMarkup:
    """Tic-Tac-Toe 3x3 doskasi"""
    rows = []
    for r in range(3):
        row = []
        for c in range(3):
            idx = r * 3 + c
            cell_text = board[idx]
            row.append(
                InlineKeyboardButton(
                    text=cell_text,
                    callback_data=f"ttt:{game_id}:{idx}"
                )
            )
        rows.append(row)
    rows.append([
        InlineKeyboardButton(
            text="🏳️ Taslim bo'lish",
            callback_data=f"surrender:{game_id}"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def get_guess_number_setup_keyboard(game_id: str, bot_username: str) -> InlineKeyboardMarkup:
    """Son topish o'yinida maxfiy son tanlash tugmalari"""
    buttons = [
        [
            InlineKeyboardButton(
                text="🎲 Tasodifiy son berilsin",
                callback_data=f"rndnum:{game_id}"
            )
        ]
    ]
    if bot_username:
        buttons.insert(0, [
            InlineKeyboardButton(
                text="🤫 O'z sonimni kiritaman (Lichkada)",
                url=f"https://t.me/{bot_username}?start=num_{game_id}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

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
