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
        np = n.parent
        right = np!=None and n==np.right
        super()._delete(n)
        n = self.root if np==None else (np.right if right else np.left)
        if n==None: return
        while ((n.right!=None and n.right.priority>n.priority) or
               (n.left!=None and n.left.priority>n.priority)):
            if n.right==None:
                self._right_rotate(n)
            elif n.left==None:
                self._left_rotate(n)
            elif n.left.priority>n.right.priority:
                self._right_rotate(n)
            else:
                self._left_rotate(n)
