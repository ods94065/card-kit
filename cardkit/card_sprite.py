"""Functions and data for making sprites that can draw cards.

The playing card images are stored for performance reasons on a single
large spritesheet. (This is a common performance technique you'll find
in games.)

These functions help navigate that spritesheet, returning sprite
objects that can draw a portion of that spritesheet (a signle card) to
the screen.
"""
import os

import pygame

from cardkit import card_constants as ck
from cardkit import sprite

CARD_SHEET = None

CARD_SPRITE_SHEET_FILENAME = 'cards.png'

# This contains all the necessary coordinate values for working with a
# spritesheet of playing cards.
#
# We assume a certain organization of the cards in the spritesheet:
# that the set of 52 cards are arranged in 4 rows of 13 cards, each
# row representing one suit. The rows and columns are not assumed to
# be absolutely strictly laid out adjacent to each other, but they
# must form a grid. The face-down and joker images can live anywhere
# else on the spritesheet.
#
# We also assume here that all cards have the same size.
SPRITE_SHEET_DATA = {
    'cards.png': {
        # Note that all the cards overlap slightly in the Y direction.
        'suit-y-offsets': {
            ck.CLUBS: 0,
            ck.HEARTS: 102,
            ck.SPADES: 204,
            ck.DIAMONDS: 306
        },
        # Because of the way the image was downsampled, the x offsets are not
        # strictly multiples of the card width. Some cards overlap slightly.
        'rank-x-offsets': {
            ck.ACE: 0,
            ck.TWO: 73,
            ck.THREE: 146,
            ck.FOUR: 219,
            ck.FIVE: 292,
            ck.SIX: 365,
            ck.SEVEN: 438,
            ck.EIGHT: 511,
            ck.NINE: 584,
            ck.TEN: 657,
            ck.JACK: 730,
            ck.QUEEN: 803,
            ck.KING: 876
        },
        'face-down-source-position': (0, 408),
        'joker-source-position': (146, 408),
        'card-size': (74, 103)
    }
}

# As we create sprites for cards during the running of the game, we
# will stash them here so that we don't have to create them more than
# once. This assumes that the cards are immutable!
CARD_SPRITE_CACHE = {}


def load_spritesheet():
    """Load the spritesheet for a set of playing cards.

    Currently, only one spritesheet ("the" spritesheet) is supported.
    """
    global CARD_SHEET
    project_dir = os.path.dirname(os.path.abspath(__file__))
    CARD_SHEET = pygame.image.load(
        os.path.join(project_dir, "img", CARD_SPRITE_SHEET_FILENAME)
    ).convert_alpha()


def get_sprite_data(card):
    """Returns the data needed to construct a sprite for a given card.

    Arguments:
      card (Card): the card to get data for.
    Returns: a tuple of:
      - The source position (x, y) for the card on the spritesheet,
        in spritesheet coordinates
      - The size of the card as a (w, h) pair
      - The origin of the card's sprite as (x, y) relative to the
        top-left corner of the sprite region
    """
    data = SPRITE_SHEET_DATA[CARD_SPRITE_SHEET_FILENAME]
    if card.face == ck.FACE_DOWN:
        source_pos = data['face-down-source-position']
    elif card.is_joker():
        source_pos = data['joker-source-position']
    else:
        source_pos = (data['rank-x-offsets'][card.rank], data['suit-y-offsets'][card.suit])

    size = data['card-size']
    origin = (0, 0) # same for all cards - top left corner
    return (source_pos, size, origin)

def sprite_for(card):
    """Returns a sprite for a given card.

    The sprite is used to draw the card, or to get the drawing
    properties of the card.

    The spritesheet must be loaded via load_spritesheet() before
    calling this function. Otherwise, a RuntimeError will be raised.
    """
    if card in CARD_SPRITE_CACHE:
        return CARD_SPRITE_CACHE[card]

    if CARD_SHEET is None:
        raise RuntimeError(
            'Must initialize card sprite sheet by calling '
            'load_spritesheet() before your main loop')

    source_pos, size, origin = get_sprite_data(card)
    card_sprite = sprite.Sprite(CARD_SHEET, source_pos, size, origin)
    CARD_SPRITE_CACHE[card] = card_sprite
    return card_sprite
