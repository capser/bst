''' 
File: test_avl.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for an AVL balanced binary 
    search tree.  It subclasses the test class TestBST, found in 
    test_base.py. 
'''
import pickle
import random
from bst.avl import Tree
from test_base import TestBST
import unittest

class TestAVL(TestBST):

    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()
        
    def checkAVL(self,n):
        ''' In the literature, AVL trees have one property
            * In each node, the heights of the left and right subtrees can 
              differ by at most 1. '''
        if n == None:  return 0
        lHeight = self.checkAVL(n.left)
        rHeight = self.checkAVL(n.right)
        self.assertTrue(abs(lHeight-rHeight) < 2)
        self.assertEqual(n.height,1+max(lHeight,rHeight))
        return 1+max(lHeight,rHeight)

    def test_AVL_property(self):
        vals = list(range(500))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkAVL(self.bst.root)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkAVL(self.bst.root)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            del self.bst[v]
            self.checkAVL(self.bst.root)
        self.assertFalse(self.bst)

    def test_pickling(self):
        vals = list(range(50))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.checkAVL(self.bst.root)
        
        pickled_tree = pickle.dumps(self.bst)
        unpickled_tree = pickle.loads(pickled_tree)
        
        self.checkAVL(self.bst.root)
        self.checkAVL(unpickled_tree.root)

unittest.main()
