from utils.stack import Stack

class Pile(Stack):

    def __init__(self):
        self.stack = []

    def takeAllCards(self):
        cards = self.stack
        self.stack = []
        return cards    

    def placeOnTop(self, card):
        self.push(card)
