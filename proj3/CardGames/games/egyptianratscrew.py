from game_abstractions.game import Game
from persistent.hand import Hand
from persistent.deck import Deck

class EgyptianRatScrew(Game):
    
    def __init__(self, players, inQueue, outQueue):
        super().__init__("Egyptian Rat Screw", players, inQueue, outQueue, mysteryHand=True)
        self.slapConditions = []
        self.setWinCondition(self.winERS)
        self.addSlapCondition(self.doublesRule)
        self.addSlapCondition(self.sandwichRule)
        self.addRule(self.play)
        self.addRule(self.slap)
        self.deal()

    def deal(self):
        for p in self.players:
            p.setHand(Deck([], []))
        while self.deck.hasCards():
            for p in self.players:
                if self.deck.hasCards():
                    p.getHand().shuffleInCards([self.deck.draw()])

    def winERS(self, player):
        return player.getHand().size() == 52

    def play(self, msg, player):
        if player == self.getCurrentPlayer() and msg.upper() == 'PLAY':
            card = player.getHand().draw()
            self.playThisCard(player, card)
            self.nextPlayer()

    def slap(self, msg, player):
        if msg.upper() == 'SLAP' and self.isSlappable():
            player.getHand().shuffleInCards(self.discard.takeAllCards())
            self.sendMessage(self.allPlayers(), player.getName() + ' has claimed the pile!')

    def isSlappable(self):
        for condition in self.slapConditions:
            if condition():
                return True
        return False

    def addSlapCondition(self, condition):
        self.slapConditions.append(condition)

    def doublesRule(self):
        firstCard, secondCard = self.discard.peekFirst(), self.discard.peekSecond()
        return firstCard and secondCard and firstCard.getRank() == secondCard.getRank()

    def sandwichRule(self):
        firstCard, thirdCard = self.discard.peekFirst(), self.discard.peekThird()
        return firstCard and thirdCard and firstCard.getRank() == thirdCard.getRank()
