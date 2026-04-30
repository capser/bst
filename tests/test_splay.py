''' 
File: test_splay.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for a splay binary search tree.  
    It subclasses the TestBST class found in test_base.py.  
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

