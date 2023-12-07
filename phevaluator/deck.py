#  based on https://github.com/andrewhoyer/deck-of-cards/
from .card import Card
import random


class Deck:
    def reset_deck(self):
        deck = []
        for x in range(0,52):
            deck.append(Card(x))

        return deck

    def __init__(self, deck=None):

        # The order of suits and labels is specific for card ranking
        if deck is None:
            self.deck = self.reset_deck()
        else:
            self.deck = deck

    def __copy__(self):
        new = type(self)(self.deck[:])
        return new

    def shuffle(self):
        random.shuffle(self.deck)

    def get_all_cards(self):
        return self.deck

    def get_card(self, position):
        '''returns a Card object. position 1 is the top card on the deck.'''

        if 0 < position <= len(self.deck):
            return self.deck[position - 1]
        else:
            return False

    def deal_card(self):
        return self.deck.pop(0)
