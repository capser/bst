''' 
File: test_splay.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for a splay binary search tree.  It subclasses the TestBST class found in test_base.py.  As such, it results in 13 tests: 6 for testing base.py; 6 for testing splay.py using the tests in TestBST; and one test for splay.py appearing below.
'''

import random
from bst.splay import Tree
from test_base import TestBST
import unittest

class TestSplay(TestBST):

    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()

    def test_random_splay(self):
        vals = list(range(500))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.assertTrue(self.bst)
        self.assertEqual(list(range(500)),list(self.bst[:]))

        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.assertTrue(self.bst)
        self.assertEqual(list(range(500)),list(self.bst[:]))

        random.shuffle(vals)
        for v in vals:
            del self.bst[v]
        self.assertFalse(self.bst)

unittest.main()

