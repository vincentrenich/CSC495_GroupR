class Player:
    def __repr__(self):
        return self.name
        
    def __init__(self, playername):
        self.name, self.hand, = playername, None
    
    def getName(self):
        return self.name

    def startTurn(self):
        self.isPlaying = True;
    
    def endTurn(self):
        self.isPlaying = False

    def getIsPlaying(self):
        return self.isPlaying
    
    def viewHand(self):
        if self.hand == None:
            return "Empty hand."
        return str(self.hand)
        
    def getHand(self):
        return self.hand

    def numCards(self):
        return self.hand.getNumCards()

    def hasNoCards(self):
        return self.numCards() == 0
    
    def getCardsInHand(self):
        return self.hand.getCards()
    
    def setHand(self, hand):
        self.hand = hand

    def playTopCard(self):
        return self.hand.getTopCard()
    
    def playCard(self, card):
        if card in self.hand.getCards():
            return self.hand.discard(card)
