"""Player Implementation"""

import threading

class Player():
    """Card Game Player"""
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bet = 0
        self.hand = None #initialize in game - hands are different in each
        self.out = False

    def __repr__(self):
        return self.name

    def draw(self, deck):
        """Extend drawing up to the player level
        Allows player.draw() syntax instead of player.hand.draw()
        """
        if (self.hand):
            self.hand.draw(deck)
            self.score = self.hand.score
        else:
            raise Exception(f'Player {self.name} does not have any hands!')

    def list_cards(self):
        """Extend listing cards up to the player level
        Allows player.list_cards() syntax
        """
        if (self.hand):
            return self.hand.list_cards()
        else:
            raise Exception(f'Player {self.name} does not have any hands!')

    def reset(self):
        """Extend resetting hand up to the player level
        Allows player.reset() syntax"""
        if (self.hand):
            self.hand.reset()
            self.out = False
        else:
            raise Exception(f'Player {self.name} does not have any hands!')

    def prompt_bet(self):
        temp_bet = 0
        while temp_bet == 0:
            temp_bet = int(input(
                f'{self.name}, you have ${self.money}.'
                ' Place your bet: '))
            if (temp_bet == 0):
                print('You cannot place a zero bet, try again')
        self.bet = temp_bet


class Dealer(Player):
    pass


class HostPlayer(Player):
    """Host player of an online game"""

    def __init__(self, name, money):
        super().__init__(name, money)
        self.in_time = True

    def send_message(self, message, timeout):
        """Host machine sending messages to itself should just print"""
        print(message)
        return 0

    def reset_hand(self, timeout):
        self.reset()
        return 0

    def bet(self, amt):
        self.bet = amt
        return 0

    def prompt_play(self, game_type, game_state, timeout):
        """Prompt the host machine to play. Different options by game"""
        t = threading.Timer(timeout, self.timed_out)
        if (game_type == 'Poker'):
            opponents = game_state.players
            opponents.remove(self)
            print('Current Bets: ')
            for o in opponents:
                print(f'{o.name}: {o.bet}')
            t.start()
            action = input('Call the current highest bet, raise it, or fold?')
            t.cancel()
            #process action
            if (self.in_time):
                pass

    def timed_out(self):
        self.in_time = False
        print('You have timed out. The game will now end. \n')
        print('Press Enter to return to the menu. \n')

    def kick(self):
        """Kicking the host player ends the game for everyone"""
        pass


class RemotePlayerShell(Player):
    """Represents a remote player to the host system"""

    def __init__(self, name, money):
        super().__init__(name, money)
        self.in_time = True

    def send_message(self, message, timeout):
        """Transmit a text message to the remote machine
        If remote machine doesn't respond before timeout, raise exception
        """
        pass

    def reset_hand(self, timeout):
        """Send hand reset signal to remote machine
        If remote machine doesn't respond before timeout, raise exception
        """
        pass

    def bet(self, amt):
        """Place a bet, and also syncronize to remote"""
        self.bet = amt
        pass

    def prompt_play(game, timeout):
        """Request a move from remote machine. Different options by game
        If remote machine doesn't respond before timeout, raise exception
        """
        pass

    def kick(self):
        #send 'yer out!' signal to remote
        pass

    def update_hand(self):
        #copy hand info from host to remote
        pass


class RemotePlayer(Player):
    """Remote player of an online game"""
    def __init__(self, name, money):
        super().__init__(name, money)
        self.in_time = True

    #changed mind on this. implement a data queue received from host
    #and act on that queue
    # def receive_message(self, message, timeout):
    #     """
    #     """
    #     pass

    def reset_hand(self, timeout):
        pass

    def bet(self, amt):
        self.bet = amt

    def kick(self):
        #process 'yer out!' signal
        pass
    
    def update_hand(self):
        #process hand update from host
        pass


class AIPlayer(Player):
    """Entirely automated player"""

    def __init__(self, *args, ai=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai = ai

    def reset_hand(self, timeout):
        self.reset()

    def prompt_play(self, hand, game_state):
        """Request a play from an AI player. 
        Different AI based on game"""
        return self.ai.calculate_action(hand, game_state)

    def bet(self, amt):
        self.bet = amt

    def kick():
        pass