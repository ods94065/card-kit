import unittest

from cardkit import card
from cardkit import card_constants as ck


class CardTest(unittest.TestCase):
    def testCanCreateCardWithIntegerRank(self):
        c = card.Card(2, 'clubs')
        self.assertEqual('2', c.rank)

    def testCanCreateCardWithStringRank(self):
        c = card.Card('4', 'diamonds')
        self.assertEqual('4', c.rank)

    def testCardWithRankOfOneCreatesAce(self):
        c = card.Card(1, 'spades')
        self.assertEqual(ck.ACE, c.rank)
        c = card.Card('1', 'clubs')
        self.assertEqual(ck.ACE, c.rank)

    def testCanCreaceAceWithAceRank(self):
        c = card.Card('ace', 'spades')
        self.assertEqual(ck.ACE, c.rank)

    def testCanCreateFaceCard(self):
        c = card.Card('JACK', 'diamonds')
        self.assertEqual(ck.JACK, c.rank)
        c = card.Card('queen', 'hearts')
        self.assertEqual(ck.QUEEN, c.rank)

    def testInvalidRankThrowsException(self):
        with self.assertRaises(ValueError):
            card.Card('bogus', 'diamonds')
        with self.assertRaises(ValueError):
            card.Card(11, 'clubs')

    def testCanCreateCardWithUppercaseSuit(self):
        c = card.Card(2, 'CLUBS')
        self.assertEqual(ck.CLUBS, c.suit)

    def testCanCreateCardWithLowercaseSuit(self):
        c = card.Card('jack', 'spades')
        self.assertEqual(ck.SPADES, c.suit)

    def testInvalidSuitThrowsException(self):
        with self.assertRaises(ValueError):
            card.Card('ace', 'spuds')
        with self.assertRaises(AttributeError):
            card.Card(4, 1)

    def testCanCreateJokerUsingRank(self):
        c = card.Card('JOKER', None)
        self.assertEqual(ck.JOKER, c.rank)
        self.assertTrue(c.is_joker())
        c = card.Card('joker', None)
        self.assertEqual(ck.JOKER, c.rank)
        self.assertTrue(c.is_joker())

    def testCanCreateJokerWithSuitOfJoker(self):
        c = card.Card('joker', 'joker')
        self.assertEqual(ck.JOKER, c.rank)
        self.assertIsNone(c.suit)
        self.assertTrue(c.is_joker())

    def testJokerWithInvalidSuitThrowsException(self):
        with self.assertRaises(ValueError):
            card.Card('joker', 'hearts')

    def testJokerWithInvalidRankThrowsException(self):
        with self.assertRaises(ValueError):
            card.Card(None, 'joker')

    def testNormalCardIsNotJoker(self):
        c = card.Card(10, 'diamonds')
        self.assertFalse(c.is_joker())

    def testCardIsFaceUpByDefault(self):
        c = card.Card('king', 'clubs')
        self.assertEqual(ck.FACE_UP, c.face)

    def testCanCreateCardFaceUp(self):
        c = card.Card(8, 'diamonds', 'UP')
        self.assertEqual(ck.FACE_UP, c.face)
        c = card.Card(9, 'hearts', 'up')
        self.assertEqual(ck.FACE_UP, c.face)
        c = card.Card('joker', None, 'up')
        self.assertEqual(ck.FACE_UP, c.face)

    def testCanCreateCardFaceDown(self):
        c = card.Card(7, 'clubs', 'DOWN')
        self.assertEqual(ck.FACE_DOWN, c.face)
        c = card.Card(6, 'spades', 'down')
        self.assertEqual(ck.FACE_DOWN, c.face)
        c = card.Card('joker', None, 'down')
        self.assertEqual(ck.FACE_DOWN, c.face)

    def testInvalidFaceThrowsException(self):
        with self.assertRaises(ValueError):
            c = card.Card(5, 'hearts', 'sideways')

    def testWithFaceReturnsCardWithDifferentFace(self):
        c1 = card.Card(6, 'clubs', 'up')
        c2 = c1.with_face('down')
        self.assertEqual(c1.rank, c2.rank)
        self.assertEqual(c1.suit, c2.suit)
        self.assertEqual('up', c1.face)
        self.assertEqual('down', c2.face)

    def testEqualCardsAreEqual(self):
        c1 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        c2 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        self.assertEqual(c1, c2)

    def testUnequalCardsAreUnequal(self):
        c1 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        c2 = card.Card(ck.KING, ck.HEARTS, ck.FACE_UP)
        c3 = card.Card(ck.QUEEN, ck.SPADES, ck.FACE_UP)
        c4 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_DOWN)

        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertNotEqual(c1, c4)

    def testEqualCardsHashEqual(self):
        c1 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        c2 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        self.assertEqual(hash(c1), hash(c2))

    def testUnequalCardsHashUnequal(self):
        c1 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_UP)
        c2 = card.Card(ck.KING, ck.HEARTS, ck.FACE_UP)
        c3 = card.Card(ck.QUEEN, ck.SPADES, ck.FACE_UP)
        c4 = card.Card(ck.QUEEN, ck.HEARTS, ck.FACE_DOWN)

        self.assertNotEqual(hash(c1), hash(c2))
        self.assertNotEqual(hash(c1), hash(c3))
        self.assertNotEqual(hash(c1), hash(c4))

    def testConvertCardToString(self):
        c = card.Card(4, ck.DIAMONDS)
        self.assertEqual('4 of diamonds (face up)', str(c))
        c = card.Card(ck.ACE, ck.SPADES, ck.FACE_DOWN)
        self.assertEqual('ace of spades (face down)', str(c))
        c = card.Card(ck.JOKER, None)
        self.assertEqual('joker (face up)', str(c))
