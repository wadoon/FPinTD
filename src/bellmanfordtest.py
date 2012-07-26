__author__ = 'weigla'

from dfa import *
from itertools import repeat

from queue import PriorityQueue


def acost(str):
    if len(set(str)):
        return 1.0/len(set(str))
    return 1

def short(s):
    l = str(set(s))
    return l


def astar(dea, s):
    Q,A,d,q0,F = dea
    queue = PriorityQueue()

    queue.put( (1, (s,"")))

    #end = []
    end = {}

    limit = len(Q)*2+len(A)

    reached = set()

    while not queue.empty():
        (c,(s,witness)) = queue.get()

        for a in A:
            new_word  = witness+a
            new_state = d[s,a]
            new_cost  = acost(new_word)
            a = (new_cost, (new_state,new_word))
            
            tmp = short(new_word)            
            end[(new_state,tmp)] = new_word

          #  print(tmp)
            if (new_state,tmp) not in reached and len(new_word) <= limit:
                queue.put(a)
                reached.add((new_state,tmp))
    return end

dea = DFA("test_bellmanford.xml")

r = astar(dea,0)
for s in r:
    print(s,r[s])

print(len(astar(dea,0)))
