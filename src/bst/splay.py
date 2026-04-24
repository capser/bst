"""
File: splay.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements a balanced ordered binary tree.  The balancing code here derives from the standard splay approach available in numerous websites that a simple google search will find.  While splay trees are *not* guaranteed to be balanced, the splaying of values tends to move frequently accessed elements close to the root, resulting in average O(log(n)) performance.
"""

import bst.base as base

class Tree(base.Tree):
    def _insert(self, n):
        super()._insert(n)
        self._splay(n)

    def _find(self,v):
        n = super()._find(v)
        if n!=None: self._splay(n)
        return n
      
    def _splay(self, n):
        while n.parent != None: #node is not root
            if n.parent == self.root: #node is child of root, one rotation
                if n == n.parent.left:
                    self._right_rotate(n.parent)        # zig step
                else:
                    self._left_rotate(n.parent)         # zag step
            elif n.parent.left == n:
                if n.parent.parent.left!=None and n.parent.parent.left.left==n:
                    self._right_rotate(n.parent.parent) # zig-zig step
                    self._right_rotate(n.parent)
                elif n.parent.parent.right!=None and n.parent.parent.right.left == n:
                    self._right_rotate(n.parent)        # zig-zag step
                    self._left_rotate(n.parent)
            elif n.parent.right == n:
                if n.parent.parent.left!=None and n.parent.parent.left.right == n:
                    self._left_rotate(n.parent)         # zag-zig step
                    self._right_rotate(n.parent)
                elif n.parent.parent.right!=None and n.parent.parent.right.right == n:
                    self._left_rotate(n.parent.parent)  # zag-zag step
                    self._left_rotate(n.parent)
