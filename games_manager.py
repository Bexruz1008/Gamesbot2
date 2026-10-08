import uuid
from typing import Dict, Optional, Literal

RPSChoice = Literal["rock", "paper", "scissors"]

class GameSession:
    def __init__(
        self,
        game_id: str,
        chat_id: int,
        game_type: str,  # 'rps', 'dice', 'darts', 'basket', 'football'
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

        # Emoji duel uchun
        self.dice_emoji = self._get_dice_emoji()
        self.scores: Dict[int, int] = {}
        self.current_roller_id: Optional[int] = None

    def _get_dice_emoji(self) -> str:
        emojis = {
            "dice": "🎲",
            "darts": "🎯",
            "basket": "🏀",
            "football": "⚽"
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


# Global games manager instansiyasi
games_manager = GamesManager()
