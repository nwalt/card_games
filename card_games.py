import random
import itertools
import time

def right_pad(string, length, character):
    """Pad a string to a certain length on the right side"""
    add_len = length - len(string)
    return f'{string}{character * add_len}'

def validate_character(char, acceptable_characters):
    while True:
        check = input(char)
        if len(check > 1):
            print('Please enter only one character')
            continue
        if check not in acceptable_characters:
            print('Invalid selection, try again')
            continue
        return check


class Card():
    """Standard playing card. 
    Init choses a random suit and value if none provided."""
    suits = ('S','H','C','D')
    suits_long = {'S':'Spades','H':'Hearts','C':'Clubs','D':'Diamonds'}
    values = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')
    values_long = {
        'A':'Ace','2':'Two','3':'Three','4':'Four','5':'Five','6':'Six',
        '7':'Seven','8':'Eight','9':'Nine','10':'Ten','J':'Jack','Q':'Queen',
        'K':'King'
        }
    values_plural = {
        'A':'Aces','2':'Twos','3':'Threes','4':'Fours','5':'Fives','6':'Sixes',
        '7':'Sevens','8':'Eights','9':'Nines','10':'Tens','J':'Jacks',
        'Q':'Queens','K':'Kings'
        }
    point_values = {
        'A':14,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,
        'Q':12,'K':13
        }
    def __init__(self, suit=None, value=None):
        if (suit):
            self.suit = suit
        else:
            self.suit = Card.suits[random.randint(0,3)]
        if (value):
            self.value = value
        else:
            self.value = Card.values[random.randint(0,12)]
        self.name = f'{self.value}{self.suit}'
        self.long_name = (
            f'{Card.values_long[self.value]} of {Card.suits_long[self.suit]}')

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.long_name


class Deck():
    """Class representing standard deck(s) of cards."""
    def __init__(self, num_decks=1):
        self.ini_cards = []
        self.cards = []
        for i in range(num_decks):
            self.cards.extend(
                [Card(x,y) for x in Card.suits for y in Card.values])
            #Also Works:
            #[Card(x,y) for x,y in itertools.product(Card.suits, Card.Values)]
            self.ini_cards = self.cards

    def __len__(self):
        return len(self.cards)
    def __repr__(self):
        return str(self.cards)
    def __str__(self):
        return str(self.cards)
    def shuffle(self):
        random.shuffle(self.cards)

    def cut(self, percent, side='top'):
        """Cut the deck and use only a percent of the cards"""
        if (side == 'top'):
            self.cards = self.cards[
                0:round((percent / 100) * len(self.cards))]
        elif (side == 'bottom'):
            self.cards = self.cards[
                round((percent / 100) * len(self.cards)):len(self.cards)]

    def reset(self):
        self.cards = self.ini_cards


class Player():
    """Card Game Player"""
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = None #initialize in game - hands are different in each
        self.out = False

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


class Dealer(Player):
    pass


class BlackJackHand():
    """Class representing a blackjack-specific hand"""
    bj_scores = {
        'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,
        '8':8,'9':9,'10':10,'J':10,'Q':10,'K':10
        }
    def __init__(self):
        self.cards = []
        self.score = 0
        self.aces = 0
        self.aces_converted = 0
        self.bust = False
        self.blackjack = False

    def __repr__(self):
        return str(self.cards)

    def reset(self):
        self.cards = []
        self.card_list = []
        self.score = 0
        self.acse = 0
        self.aces_converted = 0
        self.bust = False
        self.blackjack = False

    def list_cards(self):
        """Cast cards in hand to list of strings
        For easy printing"""
        card_list = [x.name for x in self.cards]
        if (card_list is not None):
            return card_list
        else:
            return[]

    def draw(self,deck):
        """Draw a card, evaluate, and add to score"""
        self.cards.append(deck.cards.pop())
        if (self.cards[-1].value == 'A'):
            self.aces += 1
        self.score += BlackJackHand.bj_scores[self.cards[-1].value]
        #Apparently the below isn't real, despite playing this way my whole life
        # #if you draw a blackjack, score is 21 automatically
        # if (self.cards[-1].suit in ('S','C') and self.cards[-1].value == 'J'):
        #     self.score = 21
        #if you bust but have an ace, convert ace to 1
        if (self.score > 21 and (self.aces > self.aces_converted)):
            self.score += -10
            self.aces_converted += 1
        #if you draw to 7 cards without busting you win
        if (len(self.cards) >= 7 and self.score < 21):
            self.score = 21
        if (self.score == 21):
            self.blackjack = True
        if (self.score > 21):
            self.bust = True
        self.card_list = self.list_cards()


class BlackJack():
    """Main class for running a blackjack game"""
    def __init__(self):
        self.dealer = Dealer('House', 50000)
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

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return 'BlackJack'

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
            for player in self.players:
                temp_bet = 0
                while temp_bet == 0:
                    temp_bet = int(input(
                        f'{player.name}, you have ${player.money}.'
                        ' Place your bet: '))
                    if (temp_bet == 0):
                        print('You cannot place a zero bet, try again')
                player.bet = temp_bet
            self.deal()
            self.display_table()
            time.sleep(1)
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
                    time.sleep(1)
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
                        time.sleep(1)
            players_in = [x.out for x in self.players]
            while (False in players_in):
                players_in = self.hit_loop()
                if (False in players_in):
                    self.display_table()
                time.sleep(1)
            print(f'{self.dealer.name} reveals their face down card...')
            self.display_table(reveal_dealer=True)
            time.sleep(1)
            print(f'{self.dealer.name} plays...')
            self.dealer_play_loop()
            if (self.dealer.hand.bust == True):
                continue
            print(f'{right_pad(self.dealer.name, 12, " ")}: '
                f'Score: {self.dealer.hand.score}')
            #final score print and win calc
            for player in self.players:
                if (player.bet != 0):
                    time.sleep(1)
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
                    time.sleep(1)
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
        while self.dealer.hand.score < 17:
            time.sleep(1)
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
                        time.sleep(1)
                print('Round Over...')
                return None
        time.sleep(1)
        print(f'{self.dealer.name} stands\n')
        time.sleep(1)


class PokerHand():
    """Poker-specific hand"""
    hand_types = {
        'royal':10, 's_flush':9, 'four_kind':8, 'full_house':7, 'flush':6, 
        'straight':5, 'three_kind':4, 'two_pair':3, 'pair':2, 'high_card':1
        }
    hand_types_long = {
        'royal':'Royal Flush', 's_flush':'Straight Flush', 
        'four_kind':'Four of a Kind', 'full_house':'Full House', 
        'flush':'Flush', 'straight':'Straight', 
        'three_kind':'Three of a Kind', 'two_pair':'Two Pair', 'high_card':''
        }

    def __init__(self):
        self.cards = []
        self.shared_cards = [] #for hold'em
        self.final_cards = [] #selected from cards and shared in hold'em
        self.type = 'high_card' #hand type string, default lowest
        self.score = 1
        self.high_card = None #highest value card

    def __repr__(self):
        temp = (
            f'{self.cards} {PokerHand.hand_types_long[self.type]}, '
            f'{self.high_card.long_name} High')
        return temp

    def reset(self):
        self.cards = []
        self.shared_cards = []
        self.final_cards = []
        self.type = 'high_card'
        self.score = 1
        self.high_card = None

    def list_cards(self):
        """Cast cards in hand to list of strings
        For easy printing"""
        card_list = [x.name for x in self.cards]
        if (card_list is not None):
            return card_list
        else:
            return[]

    def draw(self, deck):
        """Draw one card from the deck"""
        self.cards.append(deck.cards.pop())

    def eval_hand(self):
        """Identify the score of this hand"""
        points = [Card.point_values[card.value] for card in self.cards]
        self.high_card = self.cards[points.index(max(points))]
        #How many suits are in the hand?
        suit_counts = {'S':0,'H':0,'C':0,'D':0}
        for card in self.cards:
            suit_counts[card.suit] +=1
        #How many of each value are in the hand?
        value_counts = {
        'A':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'J':0,
        'Q':0,'K':0}
        for card in self.cards:
            value_counts[card.value] += 1

        #if we only have one suit in the hand, we have a flush
        if ([x != 0 for x in suit_counts.values()].count(True) == 1):
            flush = True
        else:
            flush = False

        # if we never have more than 1 of a value, we might have a straight
        value_count_list = list(value_counts.values())
        aces_high_list = value_count_list[1:]
        aces_high_list.append(value_count_list[0])
        if (True in [x > 1 for x in value_count_list]):
            straight = False
        else:
            #generate a binary number representing the point values in hand
            #with aces low
            value_mask_str_low = '0b'
            for x in value_count_list:
                value_mask_str_low += str(x)
            value_mask_low = int(value_mask_str_low, 2)
            #with aces high
            value_mask_str_high = '0b'
            for x in aces_high_list:
                value_mask_str_high += str(x)
            value_mask_high = int(value_mask_str_high, 2)
            # if our aces high number is 0b0000000011111 and is flush
            # we have a royal flush!
            if (value_mask_high == 31 and flush == True):
                self.type == 'royal'
                self.score == PokerHand.hand_types[self.type]
                return
            #check to see if the value masks equate to any binary number with
            #all 1's next to eachother
            sequence_bins = (31,62,124,248,496,992,1984,3968,7936)
            if (value_mask_low in sequence_bins or 
                value_mask_high in sequence_bins):
                straight = True

        if (straight and flush):
            self.type = 's_flush'
            self.score = PokerHand.hand_types[self.type]
            return
        if (value_count_list.count(4) == 1):
            self.type = 'four_kind'
            self.score = PokerHand.hand_types[self.type]
            return
        if (value_count_list.count(3) == 1 and 
            value_count_list.count(2) == 1):
            self.type = 'full_house'
            self.score = PokerHand.hand_types[self.type]
            return
        if (flush):
            self.type = 'flush'
            self.score = PokerHand.hand_types[self.type]
            return
        if (straight):
            self.type = 'straight'
            self.score = PokerHand.hand_types[self.type]
            return
        if (value_count_list.count(2) == 2):
            self.type = 'two_pair'
            self.score = PokerHand.hand_types[self.type]
            return
        if (value_count_list.count(2) == 1):
            self.type = 'pair'
            self.score = PokerHand.hand_types[self.type]
            return


class FiveCard():
    """Game runner class for Five Card Draw"""
    def __init__(self):
        
        pass
    
    def __repr__(self):
        return 'Five Card Draw'
    def __str__(self):
        return 'Five Card Draw'

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return 'Five Card Draw'


class TexasHoldem():
    """Game runner class for Texas Hold'em"""
    def __init__(self):
        #what do we need for a game of this?
        pass
    
    def __repr__(self):
        return "Texas Hold'em"
    def __str__(self):
        return "Texas Hold'em"

    @classmethod
    def name(cls):
        """Return the name of the class as a string.
        Classmethod so it can be used without an instance
        """
        return "Texas Hold'em"

class Poker():
    """Prompt the user to pick a poker subtype"""
    POKER_GAMES = {'1':FiveCard, '2':TexasHoldem}

    def __init__(self):
        pass

    def run(self):
        print('Poker Types:')
        for key in POKER_GAMES:
            print(f'{key}> {POKER_GAMES[key].name()}')
        poker_number = validate_character(
            "Enter the number for the type of poker you'd like to play: ", 
            '12')
        poker = POKER_GAMES[poker_number].run()

def main():
    GAMES = {'1':BlackJack, '2':Poker, '3':Solitaire}
    print('What game would you like to play? Current Options:')
    for key in GAMES:
        print(f'{key}> {GAMES[key].name()}')
    game_number = validate_character(
        'Enter the number for the game you want: ', '123')
    #Initialize the class of the chosen game
    game = GAMES[game_number]()
    game.run()

if (__name__ == '__main__'):
    main()