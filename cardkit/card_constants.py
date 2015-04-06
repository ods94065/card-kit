"""A set of useful constants for use with cards."""

CLUBS = 'clubs'
DIAMONDS = 'diamonds'
HEARTS = 'hearts'
SPADES = 'spades'
SUITS = (CLUBS, DIAMONDS, HEARTS, SPADES)

ACE = 'ace'
TWO = '2'
THREE= '3'
FOUR = '4'
FIVE = '5'
SIX = '6'
SEVEN = '7'
EIGHT = '8'
NINE = '9'
TEN = '10'
JACK = 'jack'
QUEEN = 'queen'
KING = 'king'
RANKS = (
    ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
    JACK, QUEEN, KING)

JOKER = 'joker'

# These are expressed as (rank, suit) pairs instead of Cards so that
# we avoid circular dependencies between modules.
DECK_OF_52 = [(rank, suit) for rank in RANKS for suit in SUITS]
DECK_OF_54 = DECK_OF_52 + [(JOKER, None), (JOKER, None)]

FACE_UP = 'up'
FACE_DOWN = 'down'
FACES = (FACE_UP, FACE_DOWN)
