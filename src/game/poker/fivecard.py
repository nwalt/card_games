import concurrent.futures

from src.card import (
    Deck
)
from src.player import (
    Player, AIPlayer
)

class FiveCard():
    """Game runner class for Five Card Draw"""
    def __init__(self):
        self.deck = Deck(1) 
        self.pot = 0
        self.num_players = int(input('Number of Players? '))
        self.blind = int(input('Size of the big blind? '))
        self.start_money = int(
            input('How much money will each player have? '))
        self.register_players()
        self.players_in = self.players

    def __repr__(self):
        return 'Poker: Five Card Draw'
    def __str__(self):
        return 'Poker: Five Card Draw'

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return 'Poker: Five Card Draw'

    def register_players(self):
        self.players = []
        num_human_players = int(input('How many people are playing? (Remainder will be CPU) '))
        for i in range(1, num_human_players):
            pname = input(f'Human player {i}, what is your name? ')
            self.players.append(Player(pname, self.start_money))
        for i in range(1, self.num_players):
            self.players.append(AIPlayer(f'CPU Player {i}', self.start_money))
        self.remote_players = False

    def show_game_state(self):
        print(f'Players in: {[x for x in self.players_in]}')
        for player in self.players:
            print(f'{player.name} Current bet: ${player.bet}')


    def run(self):
        self.keep_playing = True
        while self.keep_playing == True:
            self.keep_playing = self.loop()

    def loop(self):
        ##Build to adapt for online players without having to change this!

        #all players come back in
        self.players_in = self.players
        self.deck.reset()
        self.deck.shuffle()
        #send hand reset task to all players async
        reset_dict = {}
        with concurrent.futures.ThreadPoolExecutor() as reset_exec:
            for player in self.players:
                reset_dict[player] = reset_exec.submit(
                    player.reset_hand, 60)
        #After 60 seconds all threads _should_ have reset or raised
        #this risks hanging main thread if one of the threads hangs
        for player in reset_dict:
            #if player doesn't respond, kick the player
            if (reset_dict[player].result() != 0):
                player.kick()
                self.players.remove(player)

        #collect blinds
        self.players[0].bet(self.blind // 2)
        self.pot += self.blind // 2
        self.players[0].send_message(
            f'You are small blind, '
            f'and have automatically bet {self.players[0].bet}')
        self.players[1].bet(self.blind)
        self.pot += self.blind
        self.players[1].send_message(
            f'You are big blind, '
            f'and have automatically bet {self.players[1].bet}')

        #deal
        for i in range(len(self.players)):
            for player in self.players:
                player.draw(self.deck)
        hand_dict = {}
        with concurrent.futures.ThreadPoolExecutor() as hand_exec:
            for player in self.players:
                hand_dict[player] = hand_exec.submit(
                    player.update_hand, 60)
        for player in hand_dict:
            if (hand_dict[player].result != 0):
                player.kick()
                self.players.remove(player)

        self.show_game_state()

        #first bet phase
        bets_not_equal = True
        while (bets_not_equal == True and len(self.players_in) > 1):
            #start with the player ahead of big blind
            bet_order = [x for x in range(2, len(self.players_in) + 1)] + [0, 1]
            for i in bet_order:
                other_players = bet_order
                other_players.remove(i)
                bet_dict = {}
                with concurrent.futures.ThreadPoolExecutor() as bet_pool:
                    for p_num in other_players:
                        bet_dict[self.players[p_num]] = bet_pool.submit(
                            self.players[p_num].send_message(
                            f'Waiting on {self.players[i].name} to play... ', 
                            60))
                    bet_dict[self.players[i]] = bet_pool.submit(
                        self.players[i].prompt_play(self, 60))
                for player in bet_dict:
                    if (bet_dict[player].result != 0):
                        player.kick()
                        self.players.remove(player)
            bets_not_equal = not (all(
                [bet_dict[x] == bet_dict[self.players[0]] for x in bet_dict]
            ))

        #poll players for first draw phase
        #poll players for second bet phase
        #display hands, calc winner
        #rotate the big and little blinds by re-ordering list
        self.players = self.players[1:] + self.players[:1]
        #reset deck
        self.deck.reset()


class FiveCardOnline(FiveCard):
    
    def register_players(self):
        #register players through the online lobby instead of all ai opponents
        #set up a lobby server on a webserver
        pass