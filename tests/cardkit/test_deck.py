import random
import unittest

from cardkit import card
from cardkit import card_constants as ck
from cardkit import deck


class DeckTest(unittest.TestCase):
    def testDefaultDeckHas52Cards(self):
        d = deck.Deck()
        self.assertEqual(52, len(d))

    def testCanCreateDeckWithCustomCardSet(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        self.assertEqual(4, len(d))

    def testDeckIsEmpty(self):
        d = deck.Deck([])
        self.assertTrue(d.is_empty())
        d = deck.Deck()
        self.assertFalse(d.is_empty())

    def testInitialCardsAreDealtInOrder(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        self.assertEqual(cards[0], d.deal())
        self.assertEqual(cards[1], d.deal())
        self.assertEqual(cards[2], d.deal())
        self.assertEqual(cards[3], d.deal())

    def testDealFailsIfDeckIsEmpty(self):
        d = deck.Deck([])
        with self.assertRaises(deck.DeckError):
            d.deal()

    def testDealSeveralDealsInOrder(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        dealt_cards = d.deal_several(len(cards))
        self.assertEqual(cards, dealt_cards)

    def testShuffle(self):
        # Hardcode the seed for this test.
        random.seed("foo")
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        d.shuffle()
        dealt_cards = d.deal_several(len(cards))
        # This was determined by capturing the results using the given seed.
        expected_shuffle = [cards[0], cards[3], cards[1], cards[2]]
        self.assertEqual(expected_shuffle, dealt_cards)

    def testDealRemovesCardFromDeck(self):
        d = deck.Deck()
        d.deal()
        self.assertEqual(51, len(d))

    def testDealSeveralRemovesCardsFromDeck(self):
        d = deck.Deck()
        d.deal_several(7)
        self.assertEqual(45, len(d))

    def testDealWithFaceSetsFace(self):
        d = deck.Deck([
            card.Card(ck.ACE, ck.SPADES, ck.FACE_DOWN),
            card.Card(ck.ACE, ck.SPADES, ck.FACE_UP)])
        c = d.deal(face=ck.FACE_UP)
        self.assertEqual(ck.FACE_UP, c.face)
        c = d.deal(face=ck.FACE_DOWN)
        self.assertEqual(ck.FACE_DOWN, c.face)

    def testDealSeveralWithFaceSetsFace(self):
        cards = [card.Card(ck.ACE, suit, ck.FACE_DOWN) for suit in ck.SUITS]
        d = deck.Deck(cards)
        dealt_cards = d.deal_several(2, ck.FACE_UP)
        for c in dealt_cards:
            self.assertEqual(ck.FACE_UP, c.face)

    def testPeekShowsTopCard(self):
        cards = [card.Card(ck.ACE, suit, ck.FACE_DOWN) for suit in ck.SUITS]
        d = deck.Deck(cards)
        c = d.peek()
        self.assertEqual(cards[0], c)

    def testPeekDoesNotRemoveCardFromDeck(self):
        cards = [card.Card(ck.ACE, suit, ck.FACE_DOWN) for suit in ck.SUITS]
        d = deck.Deck(cards)
        c = d.peek()
        self.assertEqual(len(cards), len(d))
        c2 = d.deal()
        self.assertEqual(c, c2)

    def testPeekFailsIfDeckIsEmpty(self):
        d = deck.Deck([])
        with self.assertRaises(deck.DeckError):
            d.peek()

    def testAddAddsCardToTopOfDeck(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        new_card = card.Card(ck.TWO, ck.CLUBS)
        d.add(new_card)
        c = d.deal()
        self.assertEqual(new_card, c)
        c = d.deal()
        self.assertEqual(cards[0], c)

    def testAddToBottomAddsCardToBottomOfDeck(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        new_card = card.Card(ck.TWO, ck.CLUBS)
        d.add(new_card, to_bottom=True)
        dealt_cards = d.deal_several(len(cards))
        self.assertEqual(cards, dealt_cards)
        c = d.deal()
        self.assertEqual(new_card, c)

    def testResetSetsDeckToOriginalCards(self):
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        d.deal_several(len(cards))
        self.assertEqual(0, len(d))
        d.reset()
        self.assertEqual(len(cards), len(d))
        dealt_cards = d.deal_several(4)
        self.assertEqual(cards, dealt_cards)

    def testResetUnshufflesDeck(self):
        random.seed("foo")
        cards = [card.Card(ck.ACE, suit) for suit in ck.SUITS]
        d = deck.Deck(cards)
        d.shuffle()
        d.reset()
        dealt_cards = d.deal_several(4)
        self.assertEqual(cards, dealt_cards)


