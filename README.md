# BST

BST is a Python library with multiple flavors of binary search trees.  The motivation here was to explore the relative code complexities of balancing, using different approaches coded as cleanly as possible.  As such, the trees were implemented as classes that derive from an unbalanced binary search tree (BST) class.  The trees supported here are:

- **base** -- does not balance the binary search tree;
- **avl** -- balances by keeping track of branch depths;
- **avl2** -- balances by keeping track of relative branch depths using balance factors;
- **red_black** -- balances by maintaining red-black properties;
- **aa** -- balances by maintaining red-black properties, where red nodes can only be added as a right subchild;
- **splay** -- balances by always rotating the last accessed node to the top; and
- **treap** -- balances by randomly prioritizing nodes and rotating to maintain a heap property.

This code derives from multiple sources:

- The splay, AVL, AVL2, and treap codes are rather standard, and a simple google search will net numerous websites. To emphasize unique balancing code, this library uses a class hierarchy to collect common procedures.  There are also a few code simplifications.  Finally, the AVL2 code replaces the standard AVL use of tree heights to compute balance factors with an approach that uses balance factors directly.
- The red-black balancing code was derived from psuedocode in the book "Introduction to Algorithms" by Thomas H. Cormen, Charles E. Leiserson, and Ronald L. Rivest.  Given a desire to fold red-black trees into the hierarchy, this code was adjusted to not use NIL nodes as suggested in the book.  This adjustment facilitated using the common code in the base BST class, and emphasizing the code unique to red-black trees.
- AA trees are similar to red-black trees, but the code is a bit simpler (about three quarters of the red-black tree code size).  The AA tree code here derives from pseudocode for AA trees found in wikipedia and its link to the paper "Balanced Search Trees Made Simple" by Arne Andersson.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install bst.  Simply `cd` to the directory with this README.md file and type the following command, possibly within a python virtual  environment.

```
python3 -m pip install -e .
```

## Usage

The API is implemented in base.py and does not follow the standard API for binary search trees.  The differences derive from a desire to be as pythonic as possible.  This requirement adjusts the API as follows.

- `tree = Tree()` - Create a tree.  
- `tree[key]` - Get the `key` from `tree` if it exists.  Otherwise it is `None`.  If the key is a slice, the value is a generator that iterates over the slice.  The only step sizes supported are 1 (the default) and -1 for iterating forward and backward respectively.  For instance, `next(tree[key::-1])` returns that data element with the greatest key less than or equal to `key`.
- `del tree[key]` - Delete an element matching `key`, and a KeyError occurs if no such element exists.  If `key` is a slice, the deleted elements are those in the slice.  For instance `del tree[:]` empties the entire tree.
- `tree += key` - Insert immutable `key` into the tree if it isn't there already.
- **Pickle** - All trees can be saved/loaded using pickle to provide persistence.
- Just like other python containers, trees evaluate to true only when they contain elements.  Thus, testing if `tree` is empty involves evaluating `not tree`.

The code below builds/uses/deletes a generic binary search tree.  To use the balanced variants, replace `bst.base` with the desired variant.  For instance `bst.red_black` would test red-black trees.  This code appears in test_example.py in the tests directory.

```python
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
```

## Developer notes

Testing uses Python's built-in unittest library, as originally suggested by a google AI.  Just as the code uses classes to factor out common code in the different tree balancing approaches, the unit tests also factor out common tests via a test class hierarchy.  Each balancing approach uses a different set of correctness properties that result in O(log(n)) performance.  These properties are tested in the unit test code.

In addition to the unit test code, there is a performance test that graphs the performances of the algorithms with respect to each other.  In this test, insertions were timed while incrementally adding values to a list and then incrementally deleting them.  As expected all algorithms exhibited O(log(n)) performance, but they are more than an order of magnitude slower than a python dictionary.  While there is a notable performance hierarchy in the plots, each point was generated by averaging a large number of calls.  Individual call performances were a lot noisier, making comparisions a lot less clear.  Ultimately the best algorithm depends on the application.  The only real take-away is that AVL2 is a definite improvement on AVL since these algorithms build identical trees.

[Insert performance for balanced and unbalanced BSTs](insertPerformance.png)

[Delete performance for balanced and unbalanced BSTs](deletePerformance.png)

In this test, the uniform spikes have not been investigated.  A candidate hypothesis for them derives from the fact that an explicit garbage collection is performed prior to each test.  These spikes might be due to garbage collection and memory acquisition.  The fact that they do not appear during deletion provides extra supporting evidence for this hypothesis.

The first surprise involved the base (unbalanced) code also exhibiting O(log(n)) performance when inserting randomly ordered data.  Not only was the base code O(log(n)), but it had the best relative performance.  This motivated adding more tests to illustrate cases where balancing is needed.  These extra tests also show places where splay tree performance spikes, even though splay trees are O(log(n)) on average.  Also, the relative performance of AVL trees motivated more research that resulted in finding code that tracked balance factors instead of branch heights, resulting in the  faster AVL2 code.  Finally, the insertion performance for AA and splay trees derives from the fact that balancing and splaying progresses all the way to the root of the tree.  The other algorithms stop lower down in the tree.  The same issue appears in the delete performance of splay trees.

Displaying performance test results uses matplotlib, which needs to be installed independently of this BST package.

## Contributing

Pull requests are welcome, especially if they result in code simplifications or performance improvements.  For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](LICENSE.txt)
