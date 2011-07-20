#!/usr/bin/env python
#
# File: test_covertree.py
# Date of creation: 11/20/08
# Copyright (c) 2007, Thomas Kollar <tkollar@csail.mit.edu>
# Copyright (c) 2011, Nil Geisweiller <ngeiswei@gmail.com>
# All rights reserved.
#
# This is a tester for the cover tree nearest neighbor algorithm.  For
# more information please refer to the technical report entitled "Fast
# Nearest Neighbors" by Thomas Kollar or to "Cover Trees for Nearest
# Neighbor" by John Langford, Sham Kakade and Alina Beygelzimer
#  
# If you use this code in your research, kindly refer to the technical
# report.

from covertree import CoverTree
from naiveknn import knn
# from pylab import plot, show
from numpy import subtract, dot, sqrt
from random import random, seed
import time
import cPickle as pickle

# TODO
# <dcrane> nilg: I'm getting an error at the "test cover tree find method" if I
#          change n_points in test_covertree.py (1000 is fine, 2000 is bad, 999
#          is fine, 998 is bad)                                           [08:18]
# <dcrane> also if you change the knn query to something besides (.5,.5), like
#          (.152,.252), it fails                                          [08:31]

def distance(p, q):
    # print "distance"
    # print "p =", p
    # print "q =", q
    x = subtract(p, q)
    return sqrt(dot(x, x))

def test_covertree():
    seed(1)

    n_points = 2000

    k = 5
    
    pts = [(random(), random()) for _ in xrange(n_points)]

    gt = time.time

    print "Build cover tree of", n_points, "2D-points"
    
    t = gt()
    ct = CoverTree(distance)
    for p in pts:
        ct.insert(p)
    b_t = gt() - t
    print "Building time:", b_t, "seconds"

    print "==== Test saving/loading (via pickle)"
    ctFileName = "test.ct"
    print "Save cover tree under", ctFileName
    t = gt()
    ct_file = open("test.ct", "w")
    pickle.dump(ct, ct_file)
    ct_file.close()
    print "Saving time:", gt() - t
    del ct_file
    del ct
    # load ct
    print "Reload", ctFileName
    t = gt()
    ct_file = open("test.ct")
    ct = pickle.load(ct_file)
    ct_file.close()
    print "Loading time:", gt() - t
    
    print "==== Test " + str(k) + "-nearest neighbors cover tree query ===="
    query = (0.5,0.5)

    # naive nearest neighbor
    t = gt()
    naive_results = knn(query, pts, distance, k)
    # print "resultNN =", resultNN
    n_t = gt() - t
    print "Time to run a naive " + str(k) + "-nn query:", n_t, "seconds"

    #cover-tree nearest neighbor
    t = gt()
    results = ct.knn(query, k)
    # print "result =", result
    ct_t = gt() - t
    print "Time to run a cover tree " + str(k) + "-nn query:", ct_t, "seconds"
    
    if all([distance(r, nr) != 0 for r, nr in zip(results, naive_results)]):
        print "NOT OK!"
        print results
        print "!="
        print naive_results
    else:
        print "OK!"
        print results
        print "=="
        print naive_results
        print "Cover tree query is", n_t/ct_t, "faster"


    # you need pylab for that
    # plot(pts[0], pts[1], 'rx')
    # plot([query[0]], [query[1]], 'go')
    # plot([naive_results[0][0]], [naive_results[0][1]], 'y^')
    # plot([results[0][0]], [results[0][1]], 'mo')

    # test knn_insert
    print "==== Test knn_insert method ===="
    t = gt()
    results2 = ct.knn_insert(query, k)
    # print "result =", result
    ct_t = gt() - t
    print "Time to run a cover tree " + str(k) + "-nn query:", ct_t, "seconds"
    
    if all([distance(r, nr) != 0 for r, nr in zip(results2, naive_results)]):
        print "NOT OK!"
        print results2
        print "!="
        print naive_results
    else:
        print "OK!"
        print results2
        print "=="
        print naive_results
        print "Cover tree query is", n_t/ct_t, "faster"
    

    # test find
    print "==== Test cover tree find method ===="
    nearest_test_query = ct.knn(query, 1)[0]
    print "nearest_test_query =", nearest_test_query
    if ct.find(query):
        print "OK!"
    else:
        print "NOT OK!"

    # printDotty prints the tree that was generated in dotty format,
    # for more info on the format, see http://graphviz.org/
    # ct.printDotty()

    # show()


if __name__ == '__main__':
    test_covertree()
