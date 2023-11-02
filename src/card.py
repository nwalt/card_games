"""Playing Cards & Decks implementation."""

import random


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