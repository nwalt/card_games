import time
import concurrent.futures
from functools import partial

from src.util import right_pad, validate_character
from src.card import Deck
from src.hand import BlackJackHand
from src.player import Player, AIPlayer
from src.ai.blackjack import BlackJackAI

class BlackJack():
    """Main class for running a blackjack game"""

    name = 'BlackJack'

    def __init__(self):
        self.dealer = AIPlayer('House', 50000, ai=BlackJackAI(level='dealer'))
        self.dealer.hand = BlackJackHand()
        self.register_players()
        deck_size = int(input('Deck Size? (Number of packs) '))
        self.deck = Deck(deck_size)
        self.deck.shuffle()
        cut = input('Cut the deck. What percent do we keep? ')
        if ('%' in cut):
            cut = cut.replace('%','')
        cut = int(cut)
        self.deck.cut(cut)
        self.round_count = 0
        print('~~~~~~~~~~~~~~~Game Start~~~~~~~~~~~~~~~~')

    def __repr__(self):
        return 'BlackJack'
    def __str__(self):
        return 'BlackJack'

    # @classmethod
    # def name(cls):
    #     """Return the name of the class as a string.
    #     Classmethod so it can be used without an instance
    #     """
    #     return 'BlackJack'

    def register_players(self):
        self.players = []
        player_count = int(input('How many people are playing? '))
        for i in range(player_count):
            temp_name = input(f"What's the name of Player {i + 1}? ")
            temp_money = input(f'How much money does {temp_name} have? ')
            player = Player(temp_name, int(temp_money))
            player.hand = BlackJackHand()
            self.players.append(player)

    def deal(self):
        """The initial deal"""
        self.dealer.draw(self.deck)
        for player in self.players:
            player.draw(self.deck)
        self.dealer.draw(self.deck)
        for player in self.players:
            player.draw(self.deck)

    def display_table(self, reveal_dealer = False):
        """Show the current status of the table"""
        #TODO Fixed width of table display with different length names
        if (reveal_dealer):
            dealer_card_0 = self.dealer.hand.card_list[0]
        else:
            dealer_card_0 = 'XX'
        print('~~~~~~~~~~~~~~Current Table~~~~~~~~~~~~~~')
        print(
            f'{right_pad(self.dealer.name, 12, " ")}: {dealer_card_0} '
            f'{" ".join(self.dealer.hand.card_list[1:])}')
        for player in self.players:
            print(f'{right_pad(player.name, 12, " ")}: '
            f'{" ".join(player.hand.card_list)}')
        print('')

    def run(self):
        self.keep_playing = True
        while self.keep_playing:
            #reset hands
            self.dealer.reset()
            for player in self.players:
                player.reset()
            self.round_count += 1
            print(f'Round: {self.round_count}')
            print(f'Cards Left: {len(self.deck)}')
            print(f'{self.dealer.name} has ${self.dealer.money}')
            with concurrent.futures.ThreadPoolExecutor() as bet_pool:
                for player in self.players:
                    bet_pool.submit(player.prompt_bet)
            print('')
            self.deal()
            self.display_table()
            time.sleep(0.5)
            player_scores = [x.hand.score for x in self.players]
            if (21 not in player_scores and self.dealer.hand.score != 21):
                pass
            elif (self.dealer.hand.score == 21):
                #if the dealer has 21 on first hand
                #collect bets from all players w/o 21
                print(f"{self.dealer.name}'s first card is "
                    f"{self.dealer.hand.card_list[0]}")
                print(f'{self.dealer.name} has 21!')
                for player in self.players:
                    if (player.score != 21):
                        print(f'{player.name} loses ${player.bet} to '
                            f'{self.dealer.name}')
                        player.money += -(player.bet)
                        self.dealer.money += player.bet
                    elif (player.score == 21):
                        print(f'{player.name} also has 21 and loses nothing.')
                    time.sleep(0.5)
                print('Round Over...')
                continue 
            elif (21 in player_scores):
                for player in self.players:
                    if (player.hand.score == 21):
                        print(f'{player.name} has 21 and collects '
                            f'${player.bet * 1.5}')
                        player.money += (player.bet * 1.5)
                        self.dealer.money += -(player.bet * 1.5) 
                        player.bet = 0
                        player.out = True
                        time.sleep(0.5)
            players_in = [x.out for x in self.players]
            while (False in players_in):
                players_in = self.hit_loop()
                if (False in players_in):
                    self.display_table()
                time.sleep(0.5)
            print(f'{self.dealer.name} reveals their face down card...')
            self.display_table(reveal_dealer=True)
            time.sleep(0.5)
            print(f'{self.dealer.name} plays...')
            self.dealer_play_loop()
            if (self.dealer.hand.bust == True):
                continue
            print(f'{right_pad(self.dealer.name, 12, " ")}: '
                f'Score: {self.dealer.hand.score}')
            #final score print and win calc
            for player in self.players:
                if (player.bet != 0):
                    time.sleep(0.5)
                    print(f'{right_pad(player.name, 12, " ")}: '
                        f'Score: {player.hand.score}')
                    if (player.hand.score > self.dealer.hand.score):
                        print(f'{player.name} beats {self.dealer.name} and '
                            f'collects ${player.bet}')
                        player.money += player.bet
                        self.dealer.money += -(player.bet)
                    elif (player.hand.score == self.dealer.hand.score):
                        print(f'{player.name} ties {self.dealer.name}')
                    elif (player.hand.score < self.dealer.hand.score):
                        print(f'{player.name} loses to {self.dealer.name} '
                            f'and forfeits ${player.bet}.')
                        player.money += -(player.bet)
                        self.dealer.money += player.bet
                    time.sleep(0.5)
            print('Round Over...')

    def hit_loop(self):
        for player in self.players:
            if (player.out):
                continue
            else:
                hit = validate_character(
                    f'{player.name}, Hit or Stand? h/s: ', 'hs')
            if (hit == 'h'):
                player.draw(self.deck)
                if (player.hand.score > 21):
                    print(f'{player.name} busts and loses ${player.bet}')
                    player.money += -(player.bet)
                    self.dealer.money += player.bet
                    player.bet = 0
                    player.hand.bust = True
                    player.out = True
            else:
                player.out = True
        players_in = [x.out for x in self.players]
        return players_in

    def dealer_play_loop(self):
        while True:
            action = self.dealer.ai.calculate_action(
                self.dealer.hand,
                # dealer doesn't need to know anything
                # but what's in their hand
                game_state=None
            )
            if action == 'hit':
                self.dealer.draw(self.deck)
                print(f'{self.dealer.name} draws '
                    f'{self.dealer.hand.card_list[-1]}')
                if (self.dealer.hand.score > 21):
                    print(f'{self.dealer.name} busts!')
                    for player in self.players:
                        if (player.bet != 0):
                            player.money += player.bet
                            self.dealer.money += -(player.bet)
                            print(f'{player.name} collects ${player.bet}')
                            time.sleep(0.5)
                            print('Round Over...')
                            break
            else:
                time.sleep(0.5)
                print(f'{self.dealer.name} stands\n')
                time.sleep(0.5)
                break