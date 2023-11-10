import time
import asyncio
import threading

from src.util import right_pad, validate_character
from src.card import Deck
from src.hand import BlackJackHand
from src.player import Player, AIPlayer
from src.game import GameData, GameLoop
from src.ai.blackjack import BlackJackAI

# TODO: replace the existing blackjack file with this one when it's ready

class BlackJackGame(GameData):
    """Represents the game state of a blackjack game.

    Effectively a dataclass.
    """

    def __init__(self):
        self.dealer = AIPlayer('House', 50000, ai=BlackJackAI(level='dealer'))
        self.dealer.hand = BlackJackHand()


class BlackJackLoop(GameLoop):
    """Handle game events and update the game state"""

    def __init__(self, tk_root, loop, game, game_lock):
        super().__init__(tk_root, loop, game, game_lock)
