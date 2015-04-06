import copy
import random

import pygame

from cardkit import card
from cardkit import card_constants as ck


DEFAULT_CARD_SET = [card.Card(rank, suit, ck.FACE_DOWN) for rank, suit in ck.DECK_OF_52]


class DeckError(Exception):
    """A runtime error encountered while doing Deck operations."""
    pass


class Deck(object):
    """An ordered, mutable collection of Cards.

    The deck has a top and a bottom. Most operations involve the top
    of the deck.

    len(deck) will give you the number of cards currently in the deck.

    Attributes:
      initial_cards (list): The initial sequence of cards that the
        deck was created with.  The deck may be reset to this initial
        state.
      cards (list): The current sequence of cards in the deck. For
        performance reasons, the topmost card is the _last_ element in
        the sequence.

    """
    def __init__(self, initial_cards=None):
        """Creates a Deck.

        Arguments:
          initial_cards (list or None): the sequence of initial cards
            to use, topmost card first.  If None, a standard deck of
            52 cards (no jokers) will be used. Note that the face of
            cards specified in the initial sequence will generally be
            preserved.
        """
        # Note: since we draw off the back of the list, we need to reverse
        # the order of the cards when we initially import them.
        if initial_cards is None:
            self.initial_cards = DEFAULT_CARD_SET[::-1]
        else:
            self.initial_cards = initial_cards[::-1]
        self.cards = copy.deepcopy(self.initial_cards)

    def __len__(self):
        return len(self.cards)

    def reset(self):
        """Reset the deck to the sequence of cards that it was created with."""
        # Make sure not to copy just the list but the cards
        # themselves.  That way, the original face up/down state will
        # be restored.
        self.cards = copy.deepcopy(self.initial_cards)

    def shuffle(self):
        """Shuffles the current contents of the deck.

        Note that this does _not_ affect the initial sequence of cards.
        """
        random.shuffle(self.cards)

    def peek(self):
        """Returns the top card from the deck, without removing it from the deck."""
        if self.is_empty():
            raise DeckError('Deck is empty')
        return self.cards[-1]

    def deal(self, face=None):
        """Deals the top card from the deck, removing it.

        Arguments:
          face (string or None): if specified, will force the returned
            Card to be face 'up' or 'down'.  By default, the value of
            the card in the deck will be preserved (e.g. a deck with
            face-down cards will deal them face-down).
        Returns (Card): the dealt card, with face modified if necessary.
        Raises: DeckError if the deck is empty.
        """
        if self.is_empty():
            raise DeckError('Deck is empty')
        dealt_card = self.cards.pop()
        if face is not None:
           dealt_card = dealt_card.with_face(face)
        return dealt_card

    def deal_several(self, count, face=None):
        """Deals several cards in a row from the top of the deck.

        Arguments:
          count (integer): The number of cards to deal.
          face (string or None): if non-None, forces cards to be dealt
            face 'up' or 'down'.
        Returns (list): the sequence of Cards dealt, in the order they
          were dealt.
        Raises: DeckError if the deck runs out of cards.
        """
        return [self.deal(face) for i in xrange(count)]

    def add(self, card, to_bottom=False):
        """Adds a card to the deck.

        Note that this does _not_ affect the initial set of cards.

        Arguments:
          card (Card): the card to add

          to_bottom (bool): Whether to add the card to the top or
            bottom of the deck.  By default, we add to the top of the
            deck.
        """
        if to_bottom:
            self.cards.insert(0, card)
        else:
            self.cards.append(card)

    def is_empty(self):
        """Returns True iff the deck has no cards left."""
        return (len(self.cards) == 0)

    def drawing_rect(self):
        """Returns the size of the deck when drawn, as a pygame.Rect.

        The top-left corner of the rect will be (0, 0).
        """
        if self.is_empty():
            return card.default_card_drawing_rect()
        else:
            return self.peek().drawing_rect()

    def draw(self, surface, location):
        """Draws the deck into the given surface at the given location.

        Currently, only the top of the deck is drawn, or an empty
        frame if the deck is empty.
        """
        if self.is_empty():
            rect = card.default_card_drawing_rect().move(location)
            pygame.draw.rect(surface, (50, 50, 120), rect, 1)
        else:
            top_card = self.peek()
            top_card.draw(surface, location)
