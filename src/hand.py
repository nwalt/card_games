"""Hand Implementations cover drawing, score tallying, resetting, etc"""

from src.card import Card

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

