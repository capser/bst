"""
File: avl.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements a balanced ordered binary tree.  The balancing code here derives from the standard AVL approach available in numerous websites that a simple google search will find.
"""

import bst.base as base

class Node(base.Node):
    __slots__ = ('height',)

    def __init__(self, key):
        super().__init__(key)
        self.height = 1
    
    def __getstate__(self): # this is for supporting pickling
        return (super().__getstate__(),self.height)
  
    def __setstate__(self,state): # this is for supporting unpickling
        baseState, height = state
        super().__setstate__(baseState)
        self.height = height
    
    def _swap(self,n):
        super()._swap(n)
        self.height, n.height = n.height, self.height
    
def height(n):
    return 0 if n==None else n.height
  
def balance_factor(n):
    return 0 if n==None else height(n.left) - height(n.right)
  
def reviseHeight(n):
    n.height = 1 + max(height(n.left), height(n.right))

class Tree(base.Tree):
    def _newNode(self,key):
        return Node(key)

    def _left_rotate(self,n):
        super()._left_rotate(n)
        reviseHeight(n)
        reviseHeight(n.parent)

    def _right_rotate(self,n):
        super()._right_rotate(n)
        reviseHeight(n)
        reviseHeight(n.parent)

    def _rebalance(self,np):
        while np != None:
            h = np.height
            if 2 <= abs(balance_factor(np)):    # np is unbalanced
                if balance_factor(np) < -1:
                    if balance_factor(np.right) > 0:
                        self._right_rotate(np.right)
                    self._left_rotate(np)
                elif balance_factor(np) > 1:
                    if balance_factor(np.left) < 0:
                        self._left_rotate(np.left)
                    self._right_rotate(np)
                np = np.parent     # respond to rotate pushing pointer down
            else:
                reviseHeight(np)
            if h==np.height: break              # np's height did not change
            np = np.parent

    def _insert(self, n):
        if not super()._insert(n): return
        self._rebalance(n.parent)
        
    def _delete(self,n):
        super()._delete(n)
        self._rebalance(n.parent)
