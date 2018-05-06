class Hand:
    def __repr__(self):
        return ', '.join([str(c) for c in self.cards])
        
    def __str__(self):
        return ', '.join([str(c) for c in self.cards])

    def __init__(self):
        self.cards = []

    def getCards(self):
        return self.cards
    
    def getNumCards(self):
        return len(self.cards)
    
    def addCards(self, cards):
        self.cards.extend(cards)
    
    def addCard(self, card):
        self.cards.append(card)
        
    def discard(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False
