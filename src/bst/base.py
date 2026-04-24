"""
File: base.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file implements a simple ordered binary search tree (BST).  As such it provides the
root classes for the balanced binary search tree data structures.
"""

class Node:
    __slots__ = ('key', 'right', 'left', 'parent')
  
    def __init__(self, key):
        self.key = key
        self.right, self.left, self.parent = None, None, None
    
    def __getstate__(self):       # this is for supporting pickling
        return (self.key, self.left, self.right)
      
    def __setstate__(self,state): # this is for supporting unpickling
        self.key, self.left, self.right = state
        self.parent = None
        if self.left != None: self.left.parent = self
        if self.right!= None: self.right.parent = self
    
    def _swap(self,n): # Swap two nodes, maintaining reverse pointers.
        if self.parent!=None:
            if self.parent.left==self: self.parent.left = n
            else:                      self.parent.right = n
        if n.parent!=None:
            if n.parent.left==n: n.parent.left = self
            else:                n.parent.right = self
        n.parent,self.parent = self.parent,n.parent

        n.left,self.left     = self.left,n.left
        if n.left!=None: n.left.parent = n
        if self.left!=None: self.left.parent = self
      
        n.right,self.right   = self.right,n.right
        if n.right!=None: n.right.parent = n
        if self.right!=None: self.right.parent = self
    
class Tree:
    def __init__(self):
        self.root = None
    
    def __iadd__(self,key):             # support tree.add(key)
        hash(key) # Raises type error if the key is mutable, node ordering keys should never change!
        n = self._newNode(key)
        self._insert(n)
        return self
      
    def __delitem__(self,key):      # support "del tree[key]"
        if isinstance(key, slice):
            if key.step not in [None,1,-1]:
                raise KeyError("Slicing non unit step sizes is not supported")
            if self.root==None: return
            if key.step==-1:
                n = self._maximum(self.root) if None == key.start else self._find(key.start)
                if key.start!=None and n.key > key.start:
                    n = self._previousNode(n)
                while n!=None and (None==key.stop or n.key > key.stop):
                    previous = self._previousNode(n)
                    self._delete(n)
                    n = previous
            else:
                n = self._minimum(self.root) if None == key.start else self._find(key.start)
                if key.start!=None and n.key < key.start:
                    n = self._nextNode(n)
                while n!=None and (None==key.stop or n.key < key.stop):
                    next = self._nextNode(n)
                    self._delete(n)
                    n = next
        else:
            n = self._find(key)
            if n == None or key != n.key:
                raise KeyError("Attempt to delete a non existent key.")
            self._delete(n)
    
    def __getitem__(self,key):      # support "k = tree[key]" and "for k in tree[key]: ..."
        if isinstance(key, slice):
            return self._getitems(key) # returns an iterator instead of a value
        else:
            n = self._find(key)
            return None if n==None or n.key!=key else key # return None if key not in tree
      
    def __bool__(self):             # support "if tree: ..."
        return self.root != None

    def __contains__(self,key):     # support "if key in tree: ..."
        n = self._find(key)
        return None!=n and n.key == key
    
    def __iter__(self):             # support "for key in tree: ..."
        return self[:]

    ### Internal support functions follow

    def _getitems(self,key):
        if key.step not in [-1,1,None]:
            raise KeyError(key)
        if self.root==None: return
        if key.step==-1:
            n = self._maximum(self.root) if None == key.start else self._find(key.start)
            if key.start!=None and n.key > key.start:
                n = self._previousNode(n)
            while n!=None and (None==key.stop or n.key > key.stop):
              oldKey = n.key
              yield n.key
              if n.key!=None:
                  n = self._previousNode(n)
              else:
                  n = self._find(oldKey)
                  if n!=None and n.key > oldKey:
                      n = self._previousNode(n)
        else:
            n = self._minimum(self.root) if None == key.start else self._find(key.start)
            if key.start!=None and n.key < key.start:
                n = self._nextNode(n)
            while n!=None and (None==key.stop or n.key < key.stop):
                oldKey = n.key
                yield n.key
                if n.key!=None:
                    n = self._nextNode(n)
                else:
                    n = self._find(oldKey)
                    if n!=None and n.key < oldKey:
                        n = self._nextNode(n)
      
    def _newNode(self,key):
        return Node(key)
    
    def _insert(self,n): # Insert node N into a tree.
        x,xParent = self.root,None
        while x != None:
            xParent = x
            if n.key == x.key:
                x._swap(n)
                if n.parent == None: self.root = n
                return False # actually overwrote node
            else:
                x = x.left if n.key < x.key else x.right
        n.parent = xParent
        if xParent == None: #newly added node is root
            self.root = n
        elif n.key < xParent.key:
            xParent.left = n
        else:
            xParent.right = n
        return True # new node inserted!
     
    def _delete(self,n):
        n.key = None
        # actual node to delete (at the bottom of the tree)
        y = n if None == n.left or None == n.right else self._minimum(n.right)
        # what to replace actually deleted node with
        x = y.left if y.right == None else y.right
    
        # Swap n with y to move removed node next to leaves, momentarily breaking ordered property
        if y!=n:
            n._swap(y)
            if y==self.root: self.root=n
            elif n==self.root: self.root=y
      
        self._transplant(n,x) # Delete the node.  This repairs the ordered property

    def _find(self,key): # find node with key, or the one before/after it if None was found
        n,nParent = self.root,None
        while n != None and key != n.key:
            nParent,n = n, n.left if key < n.key else n.right
        return nParent if n == None else n
  
    def _nextNode(self,n):
        if n.right!=None:
            return self._minimum(n.right)
        while n.parent!=None and n==n.parent.right:
            n = n.parent
        return n.parent
    
    def _previousNode(self,n):
        if n.left!=None:
            return self._maximum(n.left)
        while n.parent!=None and n==n.parent.left:
            n = n.parent
        return n.parent
      
    def _minimum(self, x):      # find minimum node in tree X
        while x.left != None:
            x = x.left
        return x
    
    def _maximum(self,x):       # find maximum node in tree X
        while x.right != None:
            x = x.right
        return x
  
    def _transplant(self, u, v): # replace node U with V (Does not touch elements of U!)
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        if v != None:
            v.parent = u.parent
      
    def _left_rotate(self, n): # put N under its right child (M)
        m = n.right
        m.left, n.right = n, m.left
    
        if n.right != None:
            n.right.parent = n
    
        self._transplant(n,m)
        n.parent = m

    def _right_rotate(self, n): # put N under its left child (M)
        m = n.left
        m.right, n.left = n, m.right
    
        if n.left != None:
            n.left.parent = n
       
        self._transplant(n,m)
        n.parent = m
