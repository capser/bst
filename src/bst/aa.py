"""
File: aa.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements a balanced ordered binary tree.  The balancing code here derives from pseudocode for AA trees found in wikipedia and its link to the paper "Balanced Search Trees Made Simple" by Arne Andersson.
"""

import bst.base as base

class Node(base.Node):
    __slots__ = ('level',)

    def __init__(self, key):
        super().__init__(key)
        self.level = 1
    
    def __getstate__(self): # this is for supporting pickling
        return (super().__getstate__(),self.level)
  
    def __setstate__(self,state): # this is for supporting unpickling
        baseState, level = state
        super().__setstate__(baseState)
        self.level = level

    def _swap(self,n):
        super()._swap(n)
        self.level, n.level = n.level, self.level

class Tree(base.Tree):
    def _newNode(self,key):
        return Node(key)

    def _skew(self,n):
        if n == None or n.left == None or n.left.level != n.level:
            return n
        self._right_rotate(n)
        return n.parent
    
    def _split(self,n):
        if (n == None or n.right == None or n.right.right == None or
            n.level != n.right.right.level):
            return n
        self._left_rotate(n)
        n.parent.level = n.parent.level+1
        return n.parent
    
    def _decrease_level(self,n):
        should_be = min(0 if n.left == None else n.left.level,
                        0 if n.right== None else n.right.level)+1
        if should_be < n.level:
            n.level = should_be
            if n.right!=None and should_be < n.right.level:
                n.right.level = should_be

    def _insert(self, n):
        if not super()._insert(n): return
        while n != None:
            n = self._split(self._skew(n)).parent
      
    def _delete(self, n):
        super()._delete(n)
        np = n.parent
        while np != None:
            level = np.level          # original optimization?
            self._decrease_level(np)
            np = self._skew(np)
            self._skew(np.right)
            if np.right!=None:
                self._skew(np.right.right)
            np = self._split(np)
            self._split(np.right)
            if np.level==level: break # original optimization?
            np = np.parent
