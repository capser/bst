''' 
File: test_red_black.py.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for an red-black balanced binary search
    tree.  It subclasses the TestBST class found in test_base.py.  
'''
import pickle
import random
from bst.red_black import Tree
from test_base import TestBST
import unittest

class TestRB(TestBST):

    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()
        
    def checkRedBlack(self,tree):
        ''' In the literature, red-black trees have 5 properties
            * Every node has a color.  -- This is assured by using a boolean 'red' 
              property on nodes
            * The root is black.       -- This is tested
            * Every leaf is a special node called NIL (with no key) -- None is used here
            * NIL is black.            -- None is black in testDepthProperty()
            * If a node is red, then it's children are black [ie no 2 red trees in a row]
              -- This is tested by testRedProperty()
            * Every path from root to leaf has the same number of black nodes.
              -- This is tested by testDepthProperty() '''
        def checkRedProperty(n):
            ''' Each red node can only have black node children, where None is always
                black. '''
            if n!=None:
                if n.red:
                    self.assertTrue((n.left==None or not n.left.red) and
                                    (n.right==None or not n.right.red))
                checkRedProperty(n.right)
                checkRedProperty(n.left)

        def checkDepthProperty(n):
            ''' All paths from root to leaves must have the same number of black nodes. '''
            if n == None: return 1
            d = checkDepthProperty(n.right)
            self.assertEqual(checkDepthProperty(n.left),d)
            return d if n.red else d+1

        self.assertTrue(tree.root==None or not tree.root.red)
        checkRedProperty(tree.root)
        checkDepthProperty(tree.root)
        
    def test_Red_Black_property(self):
        vals = list(range(500))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkRedBlack(self.bst)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            self.bst += v
            self.checkRedBlack(self.bst)
        self.assertTrue(self.bst)

        random.shuffle(vals)
        for v in vals:
            del self.bst[v]
            self.checkRedBlack(self.bst)
        self.assertFalse(self.bst)
        
    def test_pickling(self):
        vals = list(range(50))
        random.shuffle(vals)
        for v in vals:
            self.bst += v
        self.checkRedBlack(self.bst)
        
        pickled_tree = pickle.dumps(self.bst)
        unpickled_tree = pickle.loads(pickled_tree)
        
        self.checkRedBlack(self.bst)
        self.checkRedBlack(unpickled_tree)

unittest.main()
