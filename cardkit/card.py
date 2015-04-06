import pygame

from cardkit import card_constants as ck
from cardkit import card_sprite


class Card(object):
    """A playing card (specifically, a US standard playing card).

    Two cards are equal if their rank, suit, and face are equal, and
    cards may be used as keys in dictionaries. Note that comparison is
    not defined because the defined order of cards may vary from game
    to game (suit order, trump, and aces high/low, for example).

    Generally speaking, cards should be treated as immutable, and must
    not be modified after they are created.

    Jokers are supported.

    Attributes:
      rank (string): The rank of a card (2 through 10, jack, queen,
        king, ace).  Jokers have a rank of 'joker'.
      suit (string or None): The suit of a card: clubs, diamonds,
        hearts, or spades.  Jokers have a suit of None.
      face (string): Whether the card is facing 'up' or 'down'. This
        matters when the card is drawn.

    See card_constants for safer (compiler-checked) ways of expressing
    the different ranks, suits, and face possibilities.
    """
    def __init__(self, rank, suit, face='up'):
        """Create a card.

        Arguments:

          rank (string or int): The rank of the card. String case
            doesn't matter. Integers can be used for the numbered
            ranks if you wish. For a joker, use a value of 'joker'.
          suit (string): The suit of the card. String case doesn't
            matter.
          face (string): Whether the card is face 'up' or 'down'
            for drawing. By default, cards are 'up'.
        """
        self.rank, self.suit = self.validate_rank_and_suit(
            rank, suit)
        self.face = self.validate_face(face)

    def __hash__(self):
        return hash((self.face, self.rank, self.suit))

    def __eq__(self, rhs):
        return (
            (self.face, self.rank, self.suit)
            == (rhs.face, rhs.rank, rhs.suit))

    def __str__(self):
        if self.is_joker():
            return "%s (face %s)" % (self.rank, self.face)
        else:
            return "%s of %s (face %s)" % (
                self.rank, self.suit, self.face)

    def with_face(self, face):
        """Returns a new, similar Card, but with the given face.

        Raises: ValueError if the new face is invalid.
        """
        return Card(self.rank, self.suit, face)

    def is_joker(self):
        """Returns true iff the card is a joker."""
        return (self.rank == ck.JOKER)

    def validate_rank_and_suit(self, rank, suit):
        """Ensure that the rank and suit passed in are valid.

        This method also normalizes the rank and suit values.

        Returns: a (rank, suit) tuple with the normalized values.
        Raises: ValueError if the values passed in are invalid.
        """
        rank = str(rank).lower()
        if suit is not None:
            suit = suit.lower()

        if rank == ck.JOKER:
            if suit is not None and suit != ck.JOKER:
                raise ValueError('Cannot specify suit with joker')
            return (rank, None)

        if rank == '1':
            rank = ck.ACE

        if rank not in ck.RANKS:
            raise ValueError('Unknown rank specified: %s' % rank)
        if suit not in ck.SUITS:
            raise ValueError('Unknown suit specified: %s' % suit)

        return (rank, suit)

    def validate_face(self, face):
        """Ensures that the face value passed in is valid.

        This method also normalizes the face value.
        Returns: the normalized face value.
        Raises: ValueError if the value passed in is invalid.
        """
        face = face.lower()
        if face not in ck.FACES:
            raise ValueError('Unknown face specified: %s' % face)
        return face

    def drawing_rect(self):
        """Returns a pygame.Rect representing the size of the card.

        The top-left corner of the rect is (0,0).
        """
        return pygame.Rect(
            (0, 0), card_sprite.sprite_for(self).size)

    def draw(self, surface, location):
        """Draws the card on the surface at the given location."""
        card_sprite.sprite_for(self).draw(surface, location)


def default_card_drawing_rect():
    """Returns the approximate size of a card as a pygame.Rect.

    We allow for the possibility that certain cards might have sizes
    slightly different from others. We expect that this will be close
    to the actual size of each card.
    """
    return pygame.Rect(
        (0, 0), card_sprite.sprite_for(Card(ck.TWO, ck.CLUBS)).size)
