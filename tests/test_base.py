''' 
File: test_base.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements tests for a binary search tree.  It derives from the 'AI overview' result from a google search query on "testing binary search tree code python".  I have no idea who to attribute the original coding approach to.
'''
import pickle
import random
import unittest
from bst.base import Tree

class TestBST(unittest.TestCase):

    def setUp(self):
        self.bst = Tree()
        self.bst1 = Tree()
        
    def test_insert_and_search(self):
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
        
        for x in [50, 30, 70, 20, 40]:
            self.assertTrue(x in self.bst)
        
        self.assertIsNone(self.bst[10])
        self.assertEqual(self.bst[30],30)
        self.assertEqual(next(self.bst[60::-1]),50)
        self.assertEqual(next(self.bst[1000::-1]),70)
        self.assertEqual(next(self.bst[::-1]),70)

        
    def test_first(self):
        self.assertIsNone(next(self.bst[:],None))
        
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
            
        self.assertEqual(next(self.bst[:]),20)
        
    def test_slice_traversal(self):
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
        
        self.assertEqual(list(self.bst[:]), [20, 30, 40, 50, 70])
        self.assertEqual(list(self.bst[10:]), [20, 30, 40, 50, 70])
        self.assertEqual(list(self.bst[10:40]), [20, 30])
        self.assertEqual(list(self.bst[30:60]), [30, 40, 50])
        self.assertEqual(list(self.bst[45:]), [50, 70])
        self.assertEqual(list(self.bst[100:]), [])
        with self.assertRaises(KeyError):
            x= list(self.bst[::2])

    def test_slice_deletion(self):
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
        self.assertEqual(list(self.bst[:]), [20, 30, 40, 50, 70])
        del self.bst[45:]
        self.assertEqual(list(self.bst[:]), [20, 30, 40])
        for x in self.bst[:]:
            del self.bst[x]
        self.assertFalse(self.bst)
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
        self.assertEqual(list(self.bst[:]), [20, 30, 40, 50, 70])
        del self.bst[35:60]
        self.assertEqual(list(self.bst[:]), [20, 30, 70])
        del self.bst[::-1]
        self.assertFalse(self.bst)
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
        self.assertEqual(list(self.bst[:]), [20, 30, 40, 50, 70])
        del self.bst[:]
        for x in [50, 30, 70, 20, 40, 60, 80]:
            self.bst += x
        self.assertEqual(list(self.bst[:]), [20, 30, 40, 50, 60, 70, 80])
        with self.assertRaises(KeyError):
            del self.bst[::-2]

    def test_empty_tree(self):
        self.assertIsNone(next(self.bst[:],None))
        self.assertEqual(list(self.bst[:]), [])
        self.assertFalse(self.bst)
        with self.assertRaises(KeyError):
            del self.bst[10]

    def test_delete_and_empty(self):
        for x in [50, 30, 70, 20, 40]:
            self.bst += x
            
        with self.assertRaises(KeyError):
            del self.bst[10]
        with self.assertRaises(KeyError):
            del self.bst[60]
        with self.assertRaises(KeyError):
            del self.bst[100]

        del self.bst[20]
        self.assertEqual(list(self.bst[:]), [30, 40, 50, 70])
        
        self.assertEqual(self.bst[70], 70)
        del self.bst[70]
        self.assertEqual(list(self.bst[:]), [30, 40, 50])
        self.assertIsNone(self.bst[70])
        
        for x in [30, 40, 50]:
            del self.bst[x]
        
        self.assertEqual(list(self.bst[:]), [])
        self.assertFalse(self.bst)

    def test_pickling(self):
        vals = list(range(10))
        random.shuffle(vals)
        for x in vals:
            self.bst += x
            
        pickled_tree = pickle.dumps(self.bst)
        unpickled_tree = pickle.loads(pickled_tree)
        
        for x in vals:
            n = unpickled_tree._find(x)
            if n.left != None:
                self.assertEqual(n,n.left.parent)
            if n.right != None:
                self.assertEqual(n,n.right.parent)
                
        self.assertEqual(list(self.bst[:]),list(range(10)))

# Since these tests are imported to balancing subclasses, the main() call
# is not executed when the test class is imported and subclassed.

if __name__ == '__main__':
    unittest.main()
