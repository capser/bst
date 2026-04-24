''' 
File: test_avl.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for an AVL balanced binary search tree.  It subclasses the test class TestBST, found in test_base.py.  As such, it results in 13 tests: 6 in TestBST for testing base.py; 6 in TestBST for testing avl.py; and one test for avl.py appearing below.
'''
import pickle
import random
from bst.treap import Tree
from test_base import TestBST
import unittest

class TestAVL(TestBST):

    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()
        
    def checkTreap(self,n):
        ''' In the literature, AVL trees have one property
            * In each node, the heights of the left and right subtrees can differ by at most 1. '''
        if n != None:
            self.checkTreap(n.left)
            self.checkTreap(n.right)
            self.assertTrue(n.left==None or n.left.priority<n.priority)
            self.assertTrue(n.right==None or n.right.priority<n.priority)

    def test_treap_property(self):
        vals = list(range(500))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkTreap(self.bst.root)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkTreap(self.bst.root)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            del self.bst[v]
            self.checkTreap(self.bst.root)
        self.assertFalse(self.bst)

    def test_pickling(self):
        vals = list(range(50))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.checkTreap(self.bst.root)
        
        pickled_tree = pickle.dumps(self.bst)
        unpickled_tree = pickle.loads(pickled_tree)
        
        self.checkTreap(self.bst.root)
        self.checkTreap(unpickled_tree.root)

unittest.main()
