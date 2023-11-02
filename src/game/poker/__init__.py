from src.util import validate_character
from src.game.poker.fivecard import FiveCard, FiveCardOnline
from src.game.poker.holdem import TexasHoldem


class Poker():
    """Prompt the user to pick a poker subtype"""
    POKER_GAMES = {'1':FiveCard, '2':TexasHoldem}

    def __init__(self):
        pass
    
    def __repr__(self):
        return 'Poker'
    def __str__(self):
        return 'Poker'

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return 'Poker'

    def run(self):
        print('Poker Types:')
        for key in self.POKER_GAMES:
            print(f'{key}> {self.POKER_GAMES[key].name()}')
        poker_number = validate_character(
            "Enter the number for the type of poker you'd like to play: ", 
            '12')
        poker = self.POKER_GAMES[poker_number].run()