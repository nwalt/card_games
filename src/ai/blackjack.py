"""AI for blackjack. Decides whether to hit or stand."""

class BlackJackAI():
    def __init__(self, level=0):
        self.level = level

    def calculate_action(self, hand):
        action = None
        match self.level:
            case 'dealer':
                if hand.score < 17:
                   action = 'hit'
                else:
                    action = 'stand'
            case 0:
                pass
        return action