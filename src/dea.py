# -*- encoding: utf-8 -*-
"""

"""
import trap
import itertools
import os, sys, os.path, tempfile

from pprint import pprint

from itertools import product as xproduct
from functools import reduce


__author__ = 'weigla'
__date__ = '2012-05-09'


__all__ = ["DEA"]

def lazyiter(obj): 
    """
    >>> for a in lazyiter([1 ,2, 3]): print a
    1
    2
    3

    >>> for a in lazyiter(1): print a
    1
    """   
    if iterable(obj) and type(obj) is not tuple:  #tuple constraint for product automata
        return obj
    else: 
        return (obj , )

def iterwords(s): 
    """
    A function for a convinient iteration over words \in Sigma^*.  
    
    >>> iterwords("abc")
    ("a" , "b" , "c")

    >>> iterwords( ["ab" , "de" , "aq])
    ["ab" , "de" , "aq])
    
    """
    if type(s) in (list ,  tuple): 
        return s
    else: 
        return list(s)
        

class DEA(object):
    """
    Wrapper for TrAP DFAs. TrAP DFAs are list with five elements [Q,A,d, s, F]. 
    This class provides a convinient way to acccess the elements by name 
    and functions on DFAs.       
    
    This class should be handled immutable.
    """
    
  #  __slots__ =  ["_Q" , "_A" ,  "_d" ,  "_s" ,  "_F" , "_revDEA" , "_reachables",
  #                "_productautomata"
  #               ]
    
    def __init__(self, init):
        if type(init) is str:
            init = trap.load(init)

        self._revDEA =  None
        self._reachables = None
        self._reachables = None
        self._productautomata = {1:self} # memoization for productautomata

        self._Q, self._A, self._d, self._s, self._F = init


    @property 
    def Q(self):  return self._Q

    @property 
    def A(self):  return self._A

    @property
    def d(self):  return self._d

    @property
    def s(self):  return self._s

    @property
    def F(self):  return self._F
                
    @property 
    def reverse(self): 
        """get the reverse dea"""
        if self._revDEA is None: 
            self._revDEA =  DEAr(self)
        return self._revDEA    

    def __invert__(self): 
        return self.reverse
    
    def __iter__(self):
        return iter(self._tuple())

    def _tuple(self):
        """Provides the element in an five-tuple form"""
        return (self.Q, self.A, self.d, self.s, self.F)

    def __str__(self):
        return str(self._tuple())

    def __repr__(self):
        return "dea.DEA(%s)" % repr(self._tuple())

    def __contains__(self,obj):
        if obj in self.Q:
            return True

        if type(obj) is tuple and len(obj) == 3:
            s,w,e = obj
            return self.d[s,w] == e

        return False

    def __pow__(self, amount):
        if amount in self._productautomata:
            return self._productautomata[amount]

        Q = set( xproduct( self.Q, repeat = amount))
        delta = { (q,a) : tuple( map( lambda s: self.d[s,a] , q) )
                  for q in Q
                  for a in self.A}
            
        q0 = tuple(itertools.repeat( self.s, amount ))
        dea = DEA((Q, self.A, delta, q0, set()))

        self._productautomata[amount] = dea
        return dea


    def __call__(self ,  state , symbol = None, error = True):

        if symbol == None:
            symbol = state
            state = self.s

        #print(self.A,symbol, repr(list(map(lambda s: s in self.A , iterwords(symbol)))))
        assert all( map(lambda s: s in self.A , iterwords(symbol)))

        try: 
            if state in self.Q: 
                l = [state] + iterwords(symbol)
                return reduce(lambda q , s:  self.d[q , s] , l)                
            elif iterable(state): #\hat \delta  for tuple
                return map( lambda s: self(s , symbol) ,  state)
            else:        
                raise Exception("state not in self.Q nor iterable")                
        except BaseException as e:
            if error: 
                raise e
            else: 
                return {}        
    
    def __eq__(self, dea):
        #convert tuple or list
        if type(dea) in (list,tuple) and len(dea) == 5:
            dea = DEA(dea)
            
        #cmp only within DEA
        if type(dea) is not DEA:
            return False

        #quick test with id(…)
        if id(self) == id(dea):
            return True
        
        return all( (self.Q == dea.Q, 
                    self.A == dea.A,
                    self.d == dea.d,
                    self.s == dea.s,
                    self.F == dea.F))

    def todot(self):
        fmt_acceptable = "\t%s [shape=doublecircle]\n"
        fmt_line       = "\t%s -> %s [label=%s] \n"
        header ="""
digraph G {
	/* left to right */
	graph [rankdir=LR]
	node [filled=false, shape=circle]
	//start edge
	start [filled=false, color=white, label=""]

"""

        fil = tempfile.mktemp()
        with open(fil+".dot",'w') as f:
            f.write(header)
            for s,target in self.d.items():
                start, sign = s
                f.write(fmt_line % (start,target, sign ))
            for q in self.F:
                f.write(fmt_acceptable % q)
            f.write("start -> %s\n" % self.s)
            f.write("}")

        cmd = "dot -Tpng -o %s.png %s.dot" % (fil,fil)
        print("Starting: ", cmd)
        os.popen(cmd)
        cmd = "eog %s.png" % fil
        print("Starting: ", cmd)
        os.popen(cmd)

    def _precalculation(self):
        if self._reachables is None: #precalculate the reachable set
            d = {}
            for q in self.Q:
                d[q] = dict(self.search(q))
            self._reachables = d

    def reachable(self, start ,end):
        """

        :param start:
        :param end:
        :return:
        """
        assert start in self and end in self

        self._precalculation()

        try:
            return self._reachables[start][end] #returns the witness
        except KeyError: #cache miss, end not reachable
            return False

    def _searchMemoization(self, start_node, with_start):
        """almost the same as :func:search but use lazy stored pre calculated data
        :param start_noe:
        :param with_start:
        :return:
        """

        self._precalculation()
        reachables = self._reachables[start_node]
        if with_start:
            l = list(reachables.items())
            return [ (start_node,"")] + l
        else:
            return reachables.items()


    def tarjan(self):
        """
        Tarjan's Algorithm for strongly connected components.
        origin version can be found here: http://www.logarithmic.net/pfh-files/blog/01208083168/sort.py
        see [ItA]_

        :return:
        """
        result = []
        stack  = []
        low    = {}


        undiscovered = set(self.Q)

        graph = { node : set()  for node,sign in self._d.keys() }

        for s,e in self._d.items():
            graph[s[0]].add(e)


        def visit(node):
            if node in low: return

            num = len(low)
            low[node] = num
            stack_pos = len(stack)
            stack.append(node)

            for successor in graph[node]:
                visit(successor)
                low[node] = min(low[node], low[successor])

            if num == low[node]:
                component = tuple(stack[stack_pos:])
                del stack[stack_pos:]
                result.append(component)
                for item in component:
                    low[item] = len(graph)

        visit(self.s)
        #for node in self.Q:
        #    visit(node)

        d = {}
        for c in result:
            a = set(c)
            for node in a:
                d[node] = a
        return d

    def sCC(self):
        """
        strong connected components
        """
        Z =  {}
        f =  {}
        g =  {}

        for q in self.Q:
            a =  dict(self.search(q , True))
            b =  dict(self.reverse.search(q ,  True))

            Z[q] =  a.keys() &  b.keys()

            f.update( {  (q , p):  a[p] for p in a.keys() if p in Z[q] }) 
            f.update( {  (q , p):  b[p] for p in a.keys() if p in Z[q] })
                        
        return Z , f , g        

    def search(self , start_node , with_start = False, alphabet = None):
        """breadth first search on the transitiondiagram.

        :param start_node: node to begin the BFS.
        :param with_start: should @start_node be returned, too
        :param alphabet: the alphabet that should be used
        """
        saveAlphabet = alphabet

        if alphabet is None:
            alphabet =  self.A
        
        assert alphabet <= self.A
        assert start_node in self.Q            

        if saveAlphabet is None and self._reachables: #we have only precalculated without alphabet restriction
            result =  self._searchMemoization(start_node, with_start)
            for r in result:
                yield r


        queue     =  [start_node]
        reached   =  set()
        witnesses =  { start_node:  ""}

        if with_start: 
            #reached.add(start_node) #not important
            yield start_node ,  ""

        while queue: 
            current =  queue.pop()
            for a in alphabet:
                reachables =  self(current , a , False)
                #TODO maybe better if check for reachable in Q
                for new in lazyiter(reachables):  # only for support of reverse dea
                    if new not in reached: 
                        reached.add(new)
                        witnesses[new] =  witnesses[current] + a
                        queue.append(new)
                        yield new ,  witnesses[new]
                            
            
class DEAr(DEA): 
    """
    Should not constructed directly by the user.

    >>> d =  DEA("dea1.xml")
    >>> r =  ~d
    """
    #__slots__ =  ["_Q" , "_A" ,  "_d" ,  "_s" ,  "_F" ,  "_dea"]
     
    def __init__(self , dea): 
        Q , A , d , s , F =  dea 

        self._Q =  dea.Q
        self._A =  dea.A
        self._s =  dea.F
        self._F =  {dea.s}

        self._d =  dict()

        for q in dea.Q:  
            for a in dea.A: 
                p =  dea.d[q , a]
                #print(" %s - %s ->%s" % (p , a , q))
                try: 
                    self._d[p , a].add(q)
                except KeyError: 
                    self._d[p , a] =  {q}

        self._reachables = None

    def __invert__(self): 
        return self._dea

