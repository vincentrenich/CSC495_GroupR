from game_abstractions.game import Game
from game_abstractions.rules import *
from persistent.deck import Deck
from persistent.hand import Hand
from persisent.card import Card


class Sequence(Game):
    def __init__(self, players, inQueue, outQueue):
        super().__init__("Sequence", players, inQueue, outQueue)
        self.playRules = []
        self.setWinCondition(self.winSequence)
        self.addRule(self.queryHand)
        self.addRule(self.queryOthersCardNums)
        self.addRule(self.play)
        self.addPlayRule(self.startSuitRule)
        self.addPlayRule(self.aceRule)
        self.addPlayRule(self.normalPlayRule)
        self.deal()
        self.playedAce = self.sampleNextPlayer()
        for p in self.players:
            self.sendMessage(self.thisPlayer(p), p.viewHand())
        self.sendMessage(self.otherPlayers(self.playedAce), 'It is ' + str(self.playedAce) + "'s turn to play.")
        self.sendMessage(self.thisPlayer(self.playedAce), 'It is your turn. Play your lowest card of
        any suit.')

    def deal(self):
        for p in self.players:
            p.setHand(Hand())
        while self.deck.hasCards():
            for p in self.players:
                if self.deck.hasCards():
                    p.getHand().addCard(self.deck.draw())

    def winSequence(self, player):
        return player.hasNoCards()

    def queryHand(self, msg, player):
        if msg.upper() == 'HAND':
            self.sendMessage(self.thisPlayer(player), player.viewHand())

    def queryOthersCardNums(self, msg, player):
        if msg.upper() == 'OTHERS':
            self.sendMessage(self.thisPlayer(player), self.othersHands(player))

    def lowerRank(self, thisCard, otherCard):
        rankOrder = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        thisRank, otherRank = thisCard.getRank(), otherCard.getRank()
        return rankOrder.index(thisRank) < rankOrder.index(otherRank) 

    def canNormalPlay(self, card):
        topCard = self.getTopCard()
        return not self.playedAce and cardIs(card, suit=topCard.getSuit(), rank=self.nextRank(topCard.getRank()))

    def canSpecialPlay(self, player, card):
        if self.playedAce and player == self.playedAce:
            for c in player.getCardsInHand():
                if c.getSuit == card.getSuit and self.lowerRank(c.getRank(), card.getRank()):
                    return False
            return True

    def aceRule(self, player, card):
        if cardIs(card, rank='A') and self.canNormalPlay(card):
            self.playCard(player, card, card)
            self.playedAce = player
            self.sendMessage(self.thisPlayer(self.playedAce), 'Play your lowest card of any suit.')
            return True

    def normalPlayRule(self, player, card):
        if self.canNormalPlay(card):
            self.playCard(player, card, card)

    def startSuitRule(self, player, card):
        if self.canSpecialPlay(player, card):
            self.playCard(player, card, card)
            if not card.getRank == 'A':
                self.playedAce = None

    def play(self, msg, player):
        if player == self.getCurrentPlayer():
            if firstWord(msg) == 'PLAY':
                card, subCard, numTokens = self.extractCard(msg, player, 1)
                if not numTokens:
                    self.sendMessage(self.thisPlayer(player), 'Invalid Card')
                    return
                for r in self.playRules:
                    if r(msg, player, card, subCard, numTokens):
                        return

    def addPlayRule(self, rule):
        self.playRules.append(rule)
