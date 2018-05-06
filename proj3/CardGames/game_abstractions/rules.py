class Rules:
    
    def __init__(self):
        pass

def cardIs(card, *, rank=None, suit=None):
    if not rank and not suit:
        raise Exception("Invalid isCard use. Must define rank or suit.")
    if rank and not card.getRank() == rank:
        return False
    if suit and not card.getSuit() == suit:
        return False
    return True

def cardRankOrSuitIs(card, *, rank=None, suit=None):
    if not rank or not suit:
        raise Exception('Invalid cardRankOrSuitIs use. Should use isCard for single checks.')
    if cardIs(card, rank=rank) or cardIs(card, suit=suit):
        return True
    return False

def firstWord(msg):
    return msg.split()[0].upper()

