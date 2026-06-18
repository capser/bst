"""
File: treap.py
Author: Anthony Barrett
Date: November 4, 2025
Description: This file implements a balanced ordered binary tree.  The balancing code here derives from pseudocode for treaps found in wikipedia.
"""

import bst.base as base
from random import random

class Node(base.Node):
    __slots__ = ('priority',)

    def __init__(self, key):
        super().__init__(key)
        self.priority = random()
    
    def __getstate__(self): # this is for supporting pickling
        return (super().__getstate__(),self.priority)
  
    def __setstate__(self,state): # this is for supporting unpickling
        baseState, priority = state
        super().__setstate__(baseState)
        self.priority = priority

    def _swap(self,n):
        super()._swap(n)
        self.priority, n.priority = n.priority, self.priority

class Tree(base.Tree):
    def _newNode(self,key):
        return Node(key)

    def _insert(self, n):
        if not super()._insert(n): return
        while n.parent != None and n.priority > n.parent.priority:
            if n == n.parent.left:
                self._right_rotate(n.parent)
            else:
                self._left_rotate(n.parent)
      
    def _delete(self, n):
        # rotate node down to a leaf
        while n.left or n.right:
            if not n.left: self._left_rotate(n)
            elif not n.right: self._right_rotate(n)
            elif n.left.priority > n.right.priority: self._right_rotate(n)
            else: self._left_rotate(n)
        # Detach leaf
        parent = n.parent
        if not parent: self.root = None
        elif parent.left == n: parent.left = None
        else: parent.right = None
