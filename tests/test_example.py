''' 
File: test_example.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file contains the example code in README.md to test 
    its correctness
'''

import random
from bst.base import Tree

# create and randomly shuffle integers
vals = list(range(200))
random.shuffle(vals)

# create a tree to insert randomly shuffled integers
t = Tree()

# insert values
for v in vals:
    t += v

# print [20,21,22,23]
print(list(t[20:23.5]))

# print False
print(23.5 in t)

# print True
print(23 in t)

# print [30, 31, 32, 33, 34, 35]
print([i for i in t if 30<=i<=35])

# get & print value 20, which is the existing value just prior to unexisting 20.5
print(next(t[20.5::-1]))

# delete all values in tree using a slice
del t[:]
    
# print True since the tree should be empty
print(not t)
