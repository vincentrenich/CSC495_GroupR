from persistent.card import Card
from utils.stack import Stack

class Deck(Stack):
    def __repr__(self):
        return self.__class__.__name__
        
    def __init__(self, suits, ranks, jokers=False):
        self.stack = [Card(rank, suit) for rank in ranks for suit in suits]
        if jokers:
            self.stack.append(Card("Joker", None))
            self.stack.append(Card("Joker", None))
        
    def deal(self, numCards):
        return [self.pop() for _ in range(numCards)]

    def shuffleInCards(self, cards):
        self.stack.extend(cards)
        self.shuffle()

    def hasCards(self):
        return self.size() > 0

    def draw(self):
        return self.pop()

    def getNumCards(self):
        return self.size()
