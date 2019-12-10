import unittest
import finalproject as fp

from unittest.mock import Mock

class TestGenre(unittest.TestCase):

    def testConstructorGenre(self):
        g1 = fp.Genre("comedy")
        g2 = fp.Genre("fantasy")
        g3 = fp.Genre("action")
        g4 = fp.Genre("adventure")
        g5 = fp.Genre("animation")
        g6 = fp.Genre("biography")
        g7 = fp.Genre("crime")
        g8 = fp.Genre("family")
        g9 = fp.Genre("mystery")
        g10 = fp.Genre("horror")
        g11 = fp.Genre("romance")
        g12 = fp.Genre("war")
        g13 = fp.Genre("thriller")


        self.assertEqual(g1.genre, "comedy")
        self.assertEqual(g2.genre, "fantasy")
        self.assertEqual(g3.genre, "action")
        self.assertEqual(g4.genre, "adventure")
        self.assertEqual(g5.genre, "animation")
        self.assertEqual(g6.genre, "biography")
        self.assertEqual(g7.genre, "crime")
        self.assertEqual(g8.genre, "family")
        self.assertEqual(g9.genre, "mystery")
        self.assertEqual(g10.genre, "horror")
        self.assertEqual(g11.genre, "romance")
        self.assertEqual(g12.genre, "war")
        self.assertEqual(g13.genre, "thriller")


    def testMyGenre(self):
        g = fp.Genre("comedy")
        g2 = g.myGenre()

        self.assertIsInstance(g2, str)

    def testGetOmdbData(self):

        g = fp.Genre("comedy")
        g2 = g.getOmdbData()

        self.assertIsInstance(g2, list)
