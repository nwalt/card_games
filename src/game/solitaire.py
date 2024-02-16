from src.card import Card, Deck
from src.game import GameData, GameLoop

class SolitaireGame(GameData):
    """Represents the game state of a solitaire game.

    Effectively a dataclass.
    """

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()


class SolitaireLoop(GameLoop):
    """Handle game events and update the game state"""

    def __init__(self, tk_root, loop, game, game_lock):
        super().__init__(tk_root, loop, game, game_lock)