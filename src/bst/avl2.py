"""
File: avl2.py
Author: Anthony Barrett
Date: March 23, 2026
Description: This file implements a balanced ordered binary tree.  The balancing code derives from the AVL approach that tracks balance factors instead of tree heights.  This derives from a rather clever use of algebra to update balance factors.
"""

import bst.base as base

class Node(base.Node):
    __slots__ = ('bf',)

    def __init__(self, key):
        super().__init__(key)
        self.bf = 0
    
    def __getstate__(self): # this is for supporting pickling
        return (super().__getstate__(),self.bf)
  
    def __setstate__(self,state): # this is for supporting unpickling
        baseState, bf = state
        super().__setstate__(baseState)
        self.bf = bf
    
    def _swap(self,n):
        super()._swap(n)
        self.bf, n.bf = n.bf, self.bf
    
class Tree(base.Tree):
    def _newNode(self,key):
        return Node(key)

    def _left_rotate(self,n):
        n.bf       = n.bf       + 1 - min(0,n.right.bf)
        n.right.bf = n.right.bf + 1 + max(0,n.bf)
        super()._left_rotate(n)

    def _right_rotate(self,n):
        n.bf      = n.bf        - 1 - max(0,n.left.bf)
        n.left.bf = n.left.bf   - 1 + min(0,n.bf)
        super()._right_rotate(n)

    def _insert(self, n):
        if not super()._insert(n): return
        np = n.parent
        while np != None:
            np.bf += 1 if n == np.left else -1
            if 2 <= abs(np.bf):    # np is unbalanced
                self._balance_one(np)
                break              # np's height did not change
            elif np.bf==0: break   # np's height did not change
            n, np = np, np.parent
        
    def _delete(self,n):
        super()._delete(n)
        np,n = n.parent,n.right if n.right!=None else n.left
        while np != None:
            npp = np.parent
            b,np.bf = np.bf, (0 if np.left==np.right==None else
                              np.bf-1 if n == np.left else np.bf+1)
            if 2 <= abs(np.bf):    # np is unbalanced
                self._balance_one(np)
                np = np.parent     # respond to rotate pushing pointer down
                if np.bf!=0: break # np's height did not change
            elif b==0: break       # nP's height did not change
            n, np = np, npp

    def _balance_one(self,n):
        if n.bf < -1:
            if n.right.bf > 0:
                self._right_rotate(n.right)
            self._left_rotate(n)
        elif n.bf > 1:
            if n.left.bf < 0:
                self._left_rotate(n.left)
            self._right_rotate(n)
