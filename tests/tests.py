# -*- coding: utf-8 -*-

import unittest
import logging

import regexy
from regexy.compile import to_atoms


logging.disable(logging.CRITICAL)


def match(expression, text):
    return regexy.match(
        regexy.compile(expression),
        text)


class ReactTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_match(self):
        self.assertIsNotNone(match('a', 'a'))
        self.assertIsNotNone(match('(a)b', 'ab'))
        self.assertIsNotNone(match('(a)*', 'aa'))
        self.assertIsNotNone(match('((a)*b)', 'aab'))
        self.assertIsNotNone(match('a(b|c)*d', 'abbbbccccd'))
        self.assertIsNotNone(match('((a)*(b)*)', 'abbb'))
        self.assertIsNotNone(match('((a(b)*)*(b)*)', 'abbb'))
        self.assertIsNotNone(match('a|b', 'a'))
        self.assertIsNotNone(match('a|b', 'b'))
        self.assertIsNone(match('a(b|c)*d', 'ab'))
        self.assertIsNone(match('b', 'a'))

    def test_captures(self):
        self.assertEqual(match('(a)b', 'ab'), ('a',))
        self.assertEqual(match('(a)*', 'aa'), (('a', 'a'),))
        self.assertEqual(match('((a)*b)', 'aab'), ('aab', ('a', 'a')))
        self.assertEqual(
            match('a(b|c)*d', 'abbbbccccd'),
            (('b', 'b', 'b', 'b', 'c', 'c', 'c', 'c'),))
        self.assertEqual(
            match('((a)*(b)*)', 'abbb'),
            ('abbb', ('a',), ('b', 'b', 'b')))
        self.assertEqual(
            match('((a(b)*)*(b)*)', 'abbb'),
            ('abbb', ('abbb',), ('b', 'b', 'b'), None))
        self.assertEqual(match('(a)+', 'aa'), (('a', 'a'),))

    def test_to_atoms(self):
        self.assertEqual(to_atoms('a(b|c)*d'), 'a~(b|c)*~d')
        self.assertEqual(to_atoms('abc'), 'a~b~c')
        self.assertEqual(to_atoms('(abc|def)'), '(a~b~c|d~e~f)')
        self.assertEqual(to_atoms('(abc|def)*xyz'), '(a~b~c|d~e~f)*~x~y~z')
        self.assertEqual(to_atoms('a*b'), 'a*~b')
        self.assertEqual(to_atoms('(a)b'), '(a)~b')
        self.assertEqual(to_atoms('(a)(b)'), '(a)~(b)')

    def test_one_or_more_op(self):
        self.assertIsNotNone(match('a+', 'aaaa'))
        self.assertIsNotNone(match('ab+', 'abb'))
        self.assertIsNotNone(match('aba+', 'abaa'))
        self.assertIsNone(match('a+', ''))
        self.assertIsNone(match('a+', 'b'))
        self.assertIsNone(match('ab+', 'aab'))
