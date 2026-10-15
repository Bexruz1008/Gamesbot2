import random
import uuid
from typing import Dict, Optional, Literal, List

RPSChoice = Literal["rock", "paper", "scissors"]

class GameSession:
    def __init__(
        self,
        game_id: str,
        chat_id: int,
        game_type: str,  # 'rps', 'dice', 'darts', 'basket', 'football', 'bowling', 'roulette', 'tictactoe', 'guess_number'
        initiator_id: int,
        initiator_name: str,
        opponent_id: Optional[int] = None,
        opponent_name: Optional[str] = None,
    ):
        self.game_id = game_id
        self.chat_id = chat_id
        self.game_type = game_type
        self.initiator_id = initiator_id
        self.initiator_name = initiator_name
        self.opponent_id = opponent_id
        self.opponent_name = opponent_name
        self.status = "waiting_opponent"  # 'waiting_opponent', 'playing', 'finished'
        self.message_id: Optional[int] = None

        # RPS uchun
        self.rps_choices: Dict[int, RPSChoice] = {}

        # Emoji duel uchun (dice, darts, basket, football, bowling)
        self.dice_emoji = self._get_dice_emoji()
        self.scores: Dict[int, int] = {}
        self.current_roller_id: Optional[int] = None

        # Rus Ruletkasi uchun
        # 6 ta patron joyidan 1 tasida o'q bor (0-5)
        self.roulette_bullet = random.randint(0, 5)
        self.roulette_chamber = 0  # 0 dan 5 gacha aylanadi
        self.current_turn_id: Optional[int] = None

        # Tic-Tac-Toe (Xoch-Doira) uchun
        self.ttt_board: List[str] = ["⬜"] * 9
        self.ttt_symbols: Dict[int, str] = {}  # user_id -> '❌' yoki '⭕'

        # Son topish (1-100) uchun
        self.secret_numbers: Dict[int, int] = {}  # user_id -> tanlagan maxfiy soni
        # Raqibning sonini topish oralig'i [min, max]
        self.guess_bounds: Dict[int, List[int]] = {}

    def _get_dice_emoji(self) -> str:
        emojis = {
            "dice": "🎲",
            "darts": "🎯",
            "basket": "🏀",
            "football": "⚽",
            "bowling": "🎳"
        }
        return emojis.get(self.game_type, "🎲")

    def is_participant(self, user_id: int) -> bool:
        return user_id in (self.initiator_id, self.opponent_id)

    def get_user_name(self, user_id: int) -> str:
        if user_id == self.initiator_id:
            return self.initiator_name
        if user_id == self.opponent_id:
            return self.opponent_name or "Raqib"
        return "Ishtirokchi"

    def get_other_user_id(self, user_id: int) -> Optional[int]:
        if user_id == self.initiator_id:
            return self.opponent_id
        if user_id == self.opponent_id:
            return self.initiator_id
        return None

    def check_ttt_winner(self) -> Optional[str]:
        """Tic-Tac-Toe yutug'ini tekshirish ('❌', '⭕', 'draw' yoki None)"""
        b = self.ttt_board
        win_coords = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Gorizontal
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertikal
            (0, 4, 8), (2, 4, 6)             # Diagonal
        ]
        for c1, c2, c3 in win_coords:
            if b[c1] != "⬜" and b[c1] == b[c2] == b[c3]:
                return b[c1]
        if "⬜" not in b:
            return "draw"
        return None


class GamesManager:
    def __init__(self):
        # game_id -> GameSession
        self.games: Dict[str, GameSession] = {}

    def create_game(
        self,
        chat_id: int,
        game_type: str,
        initiator_id: int,
        initiator_name: str,
        opponent_id: Optional[int] = None,
        opponent_name: Optional[str] = None
    ) -> GameSession:
        game_id = uuid.uuid4().hex[:8]
        session = GameSession(
            game_id=game_id,
            chat_id=chat_id,
            game_type=game_type,
            initiator_id=initiator_id,
            initiator_name=initiator_name,
            opponent_id=opponent_id,
            opponent_name=opponent_name
        )
        self.games[game_id] = session
        return session

    def get_game(self, game_id: str) -> Optional[GameSession]:
        return self.games.get(game_id)

    def remove_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]

    def find_active_guess_game(self, chat_id: int, user_id: int) -> Optional[GameSession]:
        """Guruhdagi navbati kelgan son topish o'yinini topish"""
        for game in self.games.values():
            if (
                game.chat_id == chat_id
                and game.game_type == "guess_number"
                and game.status == "playing"
                and game.current_turn_id == user_id
            ):
                return game
        return None

    def find_user_waiting_guess_game(self, user_id: int) -> Optional[GameSession]:
        """Foydalanuvchi son tanlashi kutilayotgan o'yinni topish"""
        for game in self.games.values():
            if (
                game.game_type == "guess_number"
                and game.status in ("setting_numbers", "waiting_opponent")
                and game.is_participant(user_id)
                and user_id not in game.secret_numbers
            ):
                return game
        return None


# Global games manager instansiyasi
games_manager = GamesManager()

