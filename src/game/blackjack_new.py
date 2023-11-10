import time
import asyncio
import threading

from src.util import right_pad, validate_character
from src.card import Deck
from src.hand import BlackJackHand
from src.player import Player, AIPlayer
from src.ai.blackjack import BlackJackAI

# TODO: replace the existing blackjack file with this one when it's ready

class BlackJackGame:
    """Represents the game state of a blackjack game.

    Effectively a dataclass.
    """

    def __init__(self):
        self.dealer = AIPlayer('House', 50000, ai=BlackJackAI(level='dealer'))
        self.dealer.hand = BlackJackHand()


class BlackJackLoop:
    """Handle game events and update the game state"""

    def __init__(self, tk_root, loop, game, game_lock):
        # needs an event queue for game events
        # and to be aware of the tk root window 
        # so it can send tk events to the main thread
        self.tk_root = tk_root
        self.game = game
        self.game_lock = game_lock
        self.loop = loop
        self.stop_event = asyncio.Event()

    async def run(self):
        while not self.stop_event.is_set():
            print('Blackjack game loop function starting')
            # TODO: spawn other coroutines
            # that process game events on the queue
            # send event to main thread to update game screen
            # etc
            await asyncio.sleep(1)
            print('Blackjack game loop run function ran')
            # and continue forever

    def main(self):
        try:
            self.loop.run_until_complete(self.run())
        finally:
            self.loop.close()

    async def set_stop_event(self):
        self.stop_event.set()

    async def handle_network_events(self):
        pass

    async def update_game_state(self):
        #NOTE: threading.Lock.acquire will block the whole async event loop
        # need to acquire the lock in its own executor:
        # https://stackoverflow.com/questions/63420413/how-to-use-threading-lock-in-async-function-while-object-can-be-accessed-from-mu
        pass

    async def send_network_event(self, socket, message):
        pass