#stdlib
import time
import random
import itertools
import threading



#lib

#project
from src.util import validate_character
from src.game.blackjack import BlackJack
from src.game.poker import Poker
from src.game.solitaire import Solitaire


def main():
    GAMES = {
        '1':BlackJack,
        # '2':Poker,
        # '3':Solitaire
    }
    print('What game would you like to play? Current Options:')
    for key in GAMES:
        print(f'{key}> {GAMES[key].name}')
    game_number = validate_character(
        'Enter the number for the game you want: ', ''.join(GAMES.keys()))
    #Initialize the class of the chosen game
    game = GAMES[game_number]()
    game.run()

if (__name__ == '__main__'):
    main()