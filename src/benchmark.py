#!/usr/bin/pypy
'''
Created on Sat Dec 29 04:12:29 2012

@author: weigla
'''

__author__ = "Alexander Weigl <Alexander.Weigl@student.kit.edu>"
__date__ = "2012-12-29"
__license__ = "bsd"

from optparse import OptionParser
from pprint import pprint
import timeit, time
from pprint import pprint

import math
import sys, pickle
import dfa
import algorithms3 as alg



N = 10
COUNT = 1

STATISTICS = {
    "l12": {},
    "b12": {},
    "l1": {},
    "b1": {},
    "l32": {},
    "b32": {}
}

def time_alg(fn, dfa, stat):
    n = len(dfa.Q)
    for i in range(COUNT):
        startT = time.clock()    
        fn(dfa)
        endT = time.clock()
        try:
            stat[n].append( endT - startT )
        except:
            stat[n] = [ endT - startT]
        

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]
    
def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)


def std(lis):
    m = mean(lis)
    sqre = lambda x: (x-m)**2
    n = len(lis)
    return math.sqrt( mean(map(sqre, lis ) ) )


def aggregate_stats(stats):
    return {k : {n: (mean(l), std(l), median(l))  
                  for n,l in stats[k].items() }
            for k in stats}
        
    
def measure(dfa, stats):
    time_alg(alg.l12, dfa, stats["l12"])
    time_alg(alg.b12, dfa, stats["b12"])
    time_alg(alg.l1, dfa, stats["l1"]) 
    time_alg(alg.b1, dfa, stats["b1"])
    time_alg(alg.l32, dfa, stats["l32"])
    time_alg(alg.b32, dfa, stats["b32"])

def main():
    files = sys.argv[1:]
    for f in files:
        a = dfa.DFA(f)
        print("file: %s : %d" %(f, len(a.Q) ) )
        measure(a,STATISTICS)

    pickle.dump(STATISTICS, open("stat.data", "w"))
    pprint(STATISTICS)
    
    d = aggregate_stats(STATISTICS)
    pprint(d)
    pickle.dump(d, open("stat.data","w"))
    

if __name__ == '__main__':
    main()
