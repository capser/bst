"""
File: red_black.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements a balanced ordered binary tree.  The balancing code here derives from psuedocode in the book "Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, and Ronald L. Rivest.  This pseudocode was adjusted to not use NIL nodes as suggested in the book.  This adjustment facilitates using common code in the base binary search tree class, and emphasizing the code unique to red-black trees.
"""

import bst.base as base

class Node(base.Node):
    __slots__ = ('red',)

    def __init__(self, key):
        super().__init__(key)
        self.red = True

    def __getstate__(self): # this is for supporting pickling
        return (super().__getstate__(),self.red)
  
    def __setstate__(self,state): # this is for supporting unpickling
        baseState, red = state
        super().__setstate__(baseState)
        self.red = red

    def _swap(self,n):
        super()._swap(n)
        self.red, n.red = n.red, self.red

class Tree(base.Tree):
    def _newNode(self,key):
        return Node(key)
    
    def _insert(self, n):
        if not super()._insert(n): return
        while n.parent != None and n.parent.red:
            y = n.parent.parent.right if n.parent == n.parent.parent.left else n.parent.parent.left
            if y!=None and y.red: #case 1
                n.parent.red, y.red, n.parent.parent.red = False, False, True
                n = n.parent.parent
            elif n.parent == n.parent.parent.left: #n.parent is the left child
                #case2 or case3
                if n == n.parent.right: #case2
                    n = n.parent #marked n.parent as new n
                    self._left_rotate(n)
                #case3
                n.parent.red, n.parent.parent.red = False, True #made parent black and grandparent red
                self._right_rotate(n.parent.parent)
            else:
                if n == n.parent.left:
                    n = n.parent #marked n.parent as new n
                    self._right_rotate(n)
                n.parent.red, n.parent.parent.red = False, True #made parent black and grandparent red
                self._left_rotate(n.parent.parent)
        self.root.red = False
    
    def _delete(self,n):
        super()._delete(n)
        if n.red: return
        np = n.parent
        n = n.left if n.right == None else n.right
        # n -- current node; np -- current node's parent; ns -- current node's sibling
        while n!=self.root and (n==None or not n.red):
            ns = np.right if n==np.left else np.left
            if n == np.left:
                if ns!=None and ns.red:
                    ns.red,np.red = False,True
                    self._left_rotate(np)
                    ns =  np.right # n.parent.right
                if (None==ns.left or not ns.left.red) and (None==ns.right or not ns.right.red):
                    ns.red, n, np = True, np, np.parent
                else:
                    if None == ns.right or not ns.right.red:
                        if None!=ns.left: ns.left.red = False
                        ns.red = True
                        self._right_rotate(ns) # ns is n.parent.right, thus n and n.parent are unchanged
                        ns = np.right # n.parent.right
    
                    if ns!=None: ns.red = False if np==None else np.red
                    if np!=None: np.red = False
                    if ns!=None and ns.right!=None: ns.right.red = False
                    self._left_rotate(np)
                    n,np = self.root,None
            else:
                if ns!=None and ns.red:
                    ns.red,np.red = False,True
                    self._right_rotate(np)
                    ns = np.left # n.parent.left
                if ((None==ns.left or not ns.left.red) and
                    (None==ns.right or not ns.right.red)):
                    ns.red, n, np = True, np, np.parent
                else:
                    if None==ns.left or not ns.left.red:
                        if None!=ns.right: ns.right.red = False
                        ns.red = True
                        self._left_rotate(ns)
                        ns = np.left # n.parent.left
    
                    if ns!=None: ns.red = False if np==None else np.red
                    if np!=None: np.red = False
                    if ns!=None and ns.left!=None: ns.left.red = False
                    self._right_rotate(np)
                    n,np = self.root,None
    
        if n!=None: n.red = False
    
