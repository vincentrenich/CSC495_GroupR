from persistent.player import Player
from persistent.deck import Deck
from persistent.pile import Pile
from persistent.card import Card
import time

"""This defines the game class """

class Game:
    def __init__(self, gameName, players, inQueue, outQueue, *, jokers=False, timeLastCard=False, mysteryHand=False):
        self.name, self.currentTurn = gameName, 0
        self.msgsIn, self.msgsOut = inQueue, outQueue
        self.suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        self.ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.deck = Deck(self.suits, self.ranks, jokers)
        self.deck.shuffle()
        self.discard = Pile()
        self.setPlayers(players)
        self.winner, self.currentPlayer, self.playDirection = None, self.players[0], 1
        self.rules, self.timeLastCard, self.lastCardTime, self.mysteryHand = [], timeLastCard, None, mysteryHand

    def setWinCondition(self, condition):
        self.winCondition = condition

    def addRule(self, rule):
        self.rules.append(rule)

    def setPlayers(self, players):
        self.players = [Player(p) for p in players]
        self.numPlayers = len(players)
    
    def drawCards(self, player, numCards):
        newCards = self.deck.deal(numCards)
        player.getHand().addCards(newCards)
        self.sendMessage(self.thisPlayer(player), 'You drew: ' + ', '.join([str(c) for c in newCards]))
        self.sendMessage(self.otherPlayers(player), player.getName() + ' drew ' + str(len(newCards)) + ' cards')
   
    def nextPlayer(self):
        self.currentPlayer = self.sampleNextPlayer()
        self.sendMessage(self.otherPlayers(self.currentPlayer), 'It is ' + self.currentPlayer.getName() + "'s turn.")
        self.sendMessage(self.thisPlayer(self.currentPlayer), 'It is your turn.')
        if not self.mysteryHand:
            self.sendMessage(self.thisPlayer(self.currentPlayer), 'Your hand is: ' + self.currentPlayer.viewHand())

    def sampleNextPlayer(self):
        return self.players[self.nextPlayerIndex()]

    def reversePlay(self):
        self.playDirection *= -1

    def nextPlayerIndex(self):
        playerIndex = self.players.index(self.getCurrentPlayer())
        return (playerIndex + self.playDirection) % len(self.players)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def setWinner(self, winner):
        self.winner = winner

    def run(self):
        try:
            while not self.winner:
                self.msgsIn.waitForEvent()
                while self.msgsIn.notEmpty():
                    inMsg = self.msgsIn.dequeue()
                    player = self.getPlayer(inMsg[0])
                    msg = inMsg[1]
                    for rule in self.rules:
                        rule(msg, player)
            self.sendMessage(self.allPlayers(), self.winner.getName() + ' has won the game!')
        except Exception as e:
            self.sendMessage(self.allPlayers(), 'Game is a Draw.')

    def canonRank(self, rank):
        upperRank = rank.upper()
        if upperRank in self.ranks:
            return upperRank
        if upperRank == 'T':
            return '10'
        return None

    def canonSuit(self, suit):
        upperSuit = suit.upper()
        for s in self.suits:
            if upperSuit == s.upper() or upperSuit == s.upper()[0]:
                return s
        return None

    def getPlayerCount(self):
        return self.numPlayers

    def getPlayer(self, playername):
        for p in self.players:
            if p.getName() == playername:
                return p
    
    def thisPlayer(self, player):
        return [player.getName()]

    def otherPlayers(self, player):
        return [p.getName() for p in self.players if not p == player]

    def allPlayers(self):
        return [p.getName() for p in self.players]

    def sendMessage(self, recipients, msg):
        self.msgsOut.enqueue((recipients, msg))

    def timeDif(self, oldTime):
        return time.time() - oldTime

    def setTimer(self, player):
        self.lastCardTime = None
        if player.numCards() == 1 and self.timeLastCard:
            self.lastCardTime = (player, time.time())

    def unsetTimer(self, player):
        if self.lastCardTime and player == self.lastCardTime[0]:
            self.lastCardTime = None

    def failTimer(self, graceTime, failTime):
        if self.lastCardTime:
            dt = self.timeDif(self.lastCardTime[1])
            if dt > graceTime and dt < graceTime + failTime:
                player = self.lastCardTime[0]
                self.lastCardTime = None
                return (True, player)
        return (False, None)

    def othersHands(self, player):
        return ', '.join([p.getName() + ': ' + str(p.numCards()) for p in self.players if not p == player])

    def getValue(self, card):
        if card.getRank() in self.ranks:
            return self.ranks.index(card.getRank()) + 1
        return 0

    def getTopCard(self):
        return self.treatedCard

    def setSuit(self, suit):
        self.treatedCard.setSuit(suit)

    def nextRank(self, rank):
        if rank in self.ranks:
            rankIndex = self.ranks.index(rank)
            rankIndex += 1
            if rankIndex >= len(self.ranks):
                rankIndex -= self.ranks
            return self.ranks[rankIndex]
        return None

    def playCard(self, player, card, treatedCard):
        if not player.playCard(card):
            return
        self.discard.placeOnTop(card)
        self.treatedCard = treatedCard
        cardString = str(card)
        if not card == treatedCard:
            cardString = cardString + ' as ' + str(treatedCard)
        self.sendMessage(self.thisPlayer(player), 'You have played: ' + cardString)
        self.sendMessage(self.otherPlayers(player), player.getName() + ' has played: ' + cardString)
        if self.winCondition(player):
            self.setWinner(player)
        self.setTimer(player)
        self.canPlayAny = False

    def playThisCard(self, player, card):
        self.discard.placeOnTop(card)
        self.treatedCard = card
        cardString = str(card)
        self.sendMessage(self.thisPlayer(player), 'You have played: ' + cardString)
        self.sendMessage(self.otherPlayers(player), player.getName() + ' has played: ' + cardString)
        if self.winCondition(player):
            self.setWinner(player)
        self.setTimer(player)
        self.canPlayAny = False

    def getCard(self, msg, startIndex):
        tokens = msg.upper().split()
        if len(tokens) < startIndex + 1:
            return (None, 0)
        if tokens[startIndex] == 'JOKER':
            return (Card('Joker', None), 1)
        if len(tokens) < startIndex + 3:
            return (None, 0)
        if not tokens[startIndex + 1] == 'OF' and not tokens[startIndex + 1] == 'O':
            return (None, 0)
        rank = tokens[startIndex]
        suit = tokens[startIndex + 2]
        rank = self.canonRank(rank)
        suit = self.canonSuit(suit)
        if not rank or not suit:
            return (None, 0)
        return (Card(rank, suit), 3)

    def extractCard(self, msg, player, startIndex):
        card, numTokens = self.getCard(msg, startIndex)
        if not card or card not in player.getCardsInHand():
            return (None, None, 0)
        subCard = card
        if card.isJoker():
            subCard, subTokens = self.getCard(msg, startIndex + numTokens)
            numTokens += subTokens
            if not subCard or subCard.isJoker():
                return (None, None, 0)
        return (card, subCard, numTokens)

    def extractSuit(self, msg, startIndex):
        tokens = msg.upper().split()
        if len(tokens) < startIndex + 1:
            return (None, 0)
        suit = self.canonSuit(tokens[startIndex])
        if not suit:
            return (None, 0)
        return (suit, 1)
