''' 
File: test_aa.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for an AA balanced binary search tree.  
    It subclasses of the TestBST class found in test_base.py.  
'''
import pickle
import random
from bst.aa import Tree
from test_base import TestBST
import unittest

class TestAA(TestBST):
    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()

    def checkAA(self,n):
        ''' In the literature, AA trees have 5 properties
            * The level of every leaf node is one.
            * The level of every left child is exactly one less than that of
              its parent.
            * The level of every right child is equal to or one less than that
              of its parent.
            * The level of every right grandchild is strictly less than that 
              of its grandparent.
            * Every node of level greater than one has two children. '''
        if n!=None:
            if n.left == None and n.right == None:
                self.assertEqual(n.level,1)
            if n.left != None:
                self.assertEqual(n.level,n.left.level+1)
            if n.right != None:
                self.assertIn(n.level,[n.right.level, n.right.level+1])
            if n.right != None:
                if n.right.right != None:
                   self.assertTrue(n.level > n.right.right.level)
                if n.right.left != None:
                    self.assertTrue(n.level > n.right.left.level)
            if n.level > 1:
                self.assertTrue(n.left != None and n.right != None)
              
            self.checkAA(n.left)
            self.checkAA(n.right)

    def test_AA_property(self):
        vals = list(range(500))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkAA(self.bst.root)
        self.assertTrue(self.bst)
        
        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkAA(self.bst.root)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            del self.bst[v]
            self.checkAA(self.bst.root)
        self.assertFalse(self.bst)
        
    def test_pickling(self):
        vals = list(range(50))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.checkAA(self.bst.root)
        
        pickled_tree = pickle.dumps(self.bst)
        unpickled_tree = pickle.loads(pickled_tree)
        
        self.checkAA(self.bst.root)
        self.checkAA(unpickled_tree.root)

unittest.main()

