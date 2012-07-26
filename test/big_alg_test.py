"""
Test cases for *dea* module.
"""
__author__ = 'weigla'
__date__ = '2012-07-12'

import sys, os
import unittest
from  unittest import TestCase
from fnmatch import fnmatch

sys.path.insert(0, os.path.abspath('../src/'))

from dfa import DFA
import witnesscheck as wc

alg = __import__("algorithms1")
def setAlgorithmicModule(name):
    global alg
    alg = __import__(name)

table = {"L12":0, "B12": 1, "L1":2, "B1": 3, "L32":4}
KNOWN_ALGORITHMS = ["l12","b12", "l1","b1", "l32"]



def run(module, algname, dea):
    return getattr(module,algname)(dea)



class BigAlgorithmTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_hierarchy(self):
        for fil in os.listdir("hierarchy"):
            if not fnmatch(fil, "dea_test_*.xml"):
                continue
            dea = DFA("hierarchy/%s" % fil)            
            expected = table[fil[9:12].strip("_")]
            
            for m in map(__import__, ("algorithms1", "algorithms2")):
                for i , a in enumerate(KNOWN_ALGORITHMS):
                    witnesses = run(m,a,dea)
                    if (type(witnesses) is dict and witnesses) \
                    or (type(witnesses) is tuple and witnesses[0] and witnesses[1]):
                        c = wc.CHECKERS[a](dea,witnesses)
                        self.assertTrue(c, 
                                        "witnesschecker missed with %s in %s (%s)" % 
                                        (witnesses,fil, a))
                        
                    #if witnesses and i<=expected:
                    #    self.assertEqual(witnesses,{}, 
                    #                     "expected %s and failed at %s (file: %s)" %(expected,i,fil))
                         
