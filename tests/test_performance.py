''' 
File: test_performance.py
Author: Anthony Barrett
Date: September 23, 2025
Description: This file contains code to test the performance of the bst variants for various value insertion orders.  While AA, AVL, and Red-Black trees always exhibited O(log(n)) performance, Base (unbalanced) and Splay trees exhibited divergences from O(log(n)) under some conditions.  
'''

from time import perf_counter
import random
import gc
import bst.base as base
import bst.aa as aa
import bst.avl as avl
import bst.avl2 as avl2
import bst.red_black as rb
import bst.splay as splay
import bst.treap as treap
import matplotlib.pyplot as plt

def performanceTest(vals,tree,step,times=50):
    sit,sdt = None,None
    for i in range(times):
        it, dt = performanceTest2(vals,tree,step)
        sit = it if sit==None else [s+i for s,i in zip(sit,it)]
        sdt = dt if sdt==None else [s+i for s,i in zip(sdt,dt)]
    return [i/times for i in sit], [d/times for d in sdt]

def performanceTest2(vals,tree,step):
    gc.collect()
    
    # insert values
    times, insert_times = [], []
    for i,v in enumerate(vals):
        if i%step==0 and times!=[]:
            times, insert_times = [], insert_times + [sum(times) / len(times)]
            
        start_time = perf_counter()
        tree += v
        end_time = perf_counter()
        times = times + [end_time - start_time]
    
    # delete values
    times, delete_times = [], []
    for i,v in enumerate(vals):
        if i%step==0 and times!=[]:
            times, delete_times = [], [sum(times) / len(times)] + delete_times
            
        start_time = perf_counter()
        del tree[v]
        end_time = perf_counter()
        times = times + [end_time - start_time]
       
    return insert_times, delete_times

# create and randomly shuffle integers
#points,values = 30, list(range(3000))
#random.shuffle(values)

def plotPerformances(values,points,ordering,times=50):
    base_inserts,base_deletes = performanceTest(values,base.Tree(),int(len(values)/points),times)
    aa_inserts,aa_deletes = performanceTest(values,aa.Tree(),int(len(values)/points),times)
    avl_inserts,avl_deletes = performanceTest(values,avl.Tree(),int(len(values)/points),times)
    avl2_inserts,avl2_deletes = performanceTest(values,avl2.Tree(),int(len(values)/points),times)
    rb_inserts,rb_deletes = performanceTest(values,rb.Tree(),int(len(values)/points),times)
    splay_inserts,splay_deletes = performanceTest(values,splay.Tree(),int(len(values)/points),times)
    treap_inserts,treap_deletes = performanceTest(values,treap.Tree(),int(len(values)/points),times)

    generatePlot(values, points, base_inserts,aa_inserts,avl_inserts,avl2_inserts,rb_inserts,splay_inserts,treap_inserts,
                 title='Comparison of Average Insert Times For %s Order Insertion'%(ordering))
                 
    generatePlot(values, points, base_deletes,aa_deletes,avl_deletes,avl2_deletes,rb_deletes,splay_deletes,treap_deletes,
                 title='Comparison of Average Delete Times For %s Order Deletion'%(ordering))


def generatePlot(values, points, base, aa, avl, avl2, rb, splay, treap, title):
    x_values = range(len(base))

    plt.figure(figsize=(8, 6)) # Optional: set figure size
    # Plot each list
    plt.plot(x_values, base, marker='.', label='Base', color='black')
    plt.plot(x_values, aa, marker='.', label='AA', color='purple')
    plt.plot(x_values, avl, marker='.', label='AVL', color='blue')
    plt.plot(x_values, avl2, marker='.', label='AVL2', color='grey')
    plt.plot(x_values, rb, marker='.', label='Red/Black', color='red')
    plt.plot(x_values, splay, marker='.', label='Splay', color='green')
    plt.plot(x_values, treap, marker='.', label='Treap', color='cyan')

    # Add labels, title, and legend
    plt.xlabel('Tree with %sn to %s(n+1) Nodes'%(int(len(values)/points),int(len(values)/points)))
    plt.ylabel('Time (s)')
    plt.title(title)
    plt.legend() # Display the legend with labels

    # Show the plot
    # plt.grid(True) # Optional: add a grid
    plt.show()

# create and randomly shuffle integers
vals = list(range(50000))
random.shuffle(vals)
plotPerformances(vals,50,"Random")

plotPerformances([i for i in range(1000)],100,"In")

plotPerformances([1000-i for i in range(1000)],100,"Reverse")

plotPerformances([i*2 if i<500 else 999-i*2 for i in range(1000)],100,"Up Down")

plotPerformances([i if i%2==0 else 1000-i for i in range(1000)],100,"Up Down Interleaved")


