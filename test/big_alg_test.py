"""
Test cases for *dea* module.
"""
from __future__ import print_function

__author__ = 'weigla'
__date__ = '2012-07-12'


import sys, os, os.path
import unittest
from  unittest import TestCase
from fnmatch import fnmatch

sys.path.insert(0, os.path.abspath('../src/'))
sys.path.insert(0, os.path.abspath('src/'))

from dfa import DFA, valid_witness
import witnesscheck as wc

import algorithms1, algorithms2
import time

KNOWN_ALGORITHMS = ["l12","b12", "l1","b1", "l32"]
table            = { n.upper() : i for i,n in enumerate(KNOWN_ALGORITHMS)}


TIMES  = { (m,a) : list() 
           for a in KNOWN_ALGORITHMS 
           for m in (algorithms1, algorithms2) }

def run(module, algname, dea):
    t0 = time.time() * 1000
    return getattr(module,algname)(dea)
    t1 = time.time() * 1000
    TIMES[m,a].append(t1-t0) 

class BigAlgorithmTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_hierarchy(self):
        d = "hierarchy" 
        if not os.path.exists("hierarchy"):
            d = "test/"+d
        
        for fil in os.listdir(d):
            if not fnmatch(fil, "dea_test_*.xml"):
                continue
            dea = DFA(os.path.join(d,fil))
            print("Checking: %s" % fil, end = " ")
            #expected = table[fil[9:12].strip("_")]
            
            for m in (algorithms1, algorithms2):
                for i , a in enumerate(KNOWN_ALGORITHMS):
                    witnesses = run(m , a , dea)
                    c = wc.CHECKERS[a](dea,witnesses)                        
                    print(a, end = " ")
            print()

import math
def mean(l):
    return float(sum(l))/len(l)

def std(l):
    m = mean(l)
    return math.sqrt( mean( map ( lambda x: (x-m)**2, l)))



if __name__ == "__main__":
    unittest.main()
    for k,v in TIMES.items():
        print("%s: mean: %f std: %f" %( k, mean(v), std(v)))