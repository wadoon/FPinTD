# -*- encoding: utf-8 -*-
"""

"""

import os
import sys
import itertools
import tempfile
from itertools import product as xproduct
from functools import reduce

import trap


__author__ = 'weigla'
__date__ = '2012-05-09'

__all__ = ["DFA", "iterwords", "lazyiter", "iterable", "tarjan2dict", "valid_witness"]

Py3k = sys.version_info.major == 3


def valid_witness(witness):
    """
    """
    return bool((type(witness) is dict and witness) or (type(witness) is tuple and witness[0] and witness[1]))


def iterable(obj):
    """
    test if @obj is iterable.
    :param obj:
    :return: true iff. __iter__() exists in @obj
    """
    return hasattr(obj, "__iter__")


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
        return (obj, )


def iterwords(s):
    """
    A function for a convinient iteration over words \in Sigma^*.  
    
    >>> iterwords("abc")
    ("a" , "b" , "c")

    >>> iterwords( ["ab" , "de" , "aq])
    ["ab" , "de" , "aq])
    
    """
    if type(s) in (list, tuple):
        return s
    elif type(s) is str:
        return list(s)
    else:
        return [s, ]


def tarjan2dict(sCC):
    d = {}
    for c in sCC:
        a = set(c)
        for node in a:
            d[node] = a
    return d


class DFA(object):
    """
    Wrapper for TrAP DFAs. TrAP DFAs are list with five elements [Q,A,d, s, F]. 
    This class provides a convinient way to acccess the elements by name 
    and functions on DFAs.       
    
    This class should be handled immutable.
    """

    def __init__(self, init):
        if type(init) is str:
            self.filename = init
            init = trap.load(init)

        self._revDFA = None
        self._reachables = None
        self._reachables = None
        self._productautomata = {1: self} # memoization for productautomata

        self._Q, self._A, self._d, self._s, self._F = init

    @property
    def Q(self):
        """
        set of states
        """
        return self._Q

    @property
    def A(self):
        """
        alphabet -- set of symbols
        """
        return self._A

    @property
    def d(self):
        """
        transition table (dict)
        """
        return self._d

    @property
    def s(self):
        """
        start state with @self.s in @self.Q
        """
        return self._s

    @property
    def F(self):
        """
        set of accepting states
        """
        return self._F

    @property
    def reverse(self):
        """get the reverse dea"""
        if self._revDFA is None:
            self._revDFA = DFAr(self)
        return self._revDFA

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
        return "dfa.DFA(%s)" % repr(self._tuple())

    def __contains__(self, obj):
        if obj in self.Q:
            return True

        if type(obj) is tuple and len(obj) == 3:
            s, witness, e = obj
            return self.d[s, witness] == e

        return False

    def __pow__(self, amount):
        if amount == 1:
            return self

        if amount in self._productautomata:
            return self._productautomata[amount]

        Q = set(xproduct(self.Q, repeat=amount))
        delta = {(q, a): tuple(map(lambda s: self.d[s, a], q))
                 for q in Q
                 for a in self.A}

        q0 = tuple(itertools.repeat(self.s, amount))
        dea = DFA((Q, self.A, delta, q0, set()))

        self._productautomata[amount] = dea
        return dea


    def __call__(self, state, symbol=None, error=True):
        if symbol == None:
            symbol = state
            state = self.s

        #print(self.A,symbol, repr(list(map(lambda s: s in self.A , iterwords(symbol)))))
        if not all(map(lambda s: s in self.A, iterwords(symbol))):
            raise Exception("some char of " + str(symbol) + " is not in " + str(self.A))

        try:
            if state in self.Q:
                l = [state] + iterwords(symbol)
                return reduce(lambda q, s: self.d[q, s], l)
            elif iterable(state): #\hat \delta  for tuple
                return tuple(map(lambda s: self(s, symbol), state))
            else:
                raise Exception("state not in self.Q nor iterable")
        except BaseException as e:
            if error:
                raise e
            else:
                return []


    def __eq__(self, dea):
        #convert tuple or list
        if type(dea) in (list, tuple) and len(dea) == 5:
            dea = DFA(dea)

        #cmp only within DFA
        if type(dea) is not DFA:
            return False

        #quick test with id(…)
        if id(self) == id(dea):
            return True

        return all((self.Q == dea.Q,
                    self.A == dea.A,
                    self.d == dea.d,
                    self.s == dea.s,
                    self.F == dea.F))

    def todot(self):
        fmt_acceptable = "\t%s [shape=doublecircle]\n"
        fmt_line = "\t%s -> %s [label=%s] \n"
        header = """
digraph G {
	/* left to right */
	graph [rankdir=LR]
	node [filled=false, shape=circle]
	//start edge
	start [filled=false, color=white, label=""]

"""

        fil = tempfile.mktemp()
        with open(fil + ".dot", 'witness') as f:
            f.write(header)
            for s, target in self.d.items():
                start, sign = s
                f.write(fmt_line % (start, target, sign ))
            for q in self.F:
                f.write(fmt_acceptable % q)
            f.write("start -> %s\n" % self.s)
            f.write("}")

        cmd = "dot -Tpng -o %s.png %s.dot" % (fil, fil)
        print("Starting: ", cmd)
        os.popen(cmd)
        cmd = "eog %s.png" % fil
        os.popen(cmd)


    def tarjan(self):
        """
        Tarjan's Algorithm for strongly connected components.
        origin version can be found here: http://www.logarithmic.net/pfh-files/blog/01208083168/sort.py
        see [ItA]_

        :return:
        """
        result = []
        stack = []
        low = {}

        graph = {node: set() for node, sign in self._d.keys()}

        for s, e in self._d.items():
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

        for q in self.Q:
            visit(q)

        #visit(self.s) only for DFAs

        return result


    def sCC(self):
        """
        strong connected components
        """
        Z = {}
        f = {}
        g = {}

        for q in self.Q:
            a = dict(self.search(q, True))
            b = dict(self.reverse.search(q, True))

            if Py3k:
                Z[q] = a.keys() & b.keys()
            else:
                Z[q] = set(a.keys()) & set(b.keys())

            f.update({(q, p): a[p] for p in a.keys() if p in Z[q]})
            g.update({(q, p): b[p][::-1] for p in a.keys() if p in Z[q]})

        return Z, f, g


    def search(self, start_node, with_start=False, alphabet=None):
        """breadth first search on the transitiondiagram.

        :param start_node: node to begin the BFS.
        :param with_start: should @start_node be returned, too
        :param alphabet: the alphabet that should be used
        """
        if alphabet is None:
            alphabet = self.A

        assert alphabet <= self.A
        #assert start_node in self.Q            

        queue = [start_node]
        reached = set()
        witnesses = {start_node: ""}

        if with_start:
        #reached.add(start_node) #not important
            yield start_node, ""

        while queue:
            current = queue.pop(0)
            for a in alphabet:
                reachables = self(current, a, False)
                #TODO maybe better if check for reachable in Q
                for new in lazyiter(reachables):  # only for support of reverse dea
                    if new not in reached:
                        reached.add(new)
                        witnesses[new] = witnesses[current] + a
                        queue.append(new)
                        yield new, witnesses[new]


    def reachable(self, start, end, reflexive=False, alpha=None):
        """
        :param start:
        :param end:
        :param reflexive:
        :return:
        """
        for reached, word in self.search(start, reflexive, alpha):
            if reached == end:
                return word
        return False


    def trivialComponents(self):
        """
        :return:
        """

        def noLeavingEdges(c):
            leavingEdges = ( self(c, a) != c for a in self.A )
            return all(leavingEdges)

        sCC = self.tarjan()
        T = set()
        for comp in sCC:
            if len(comp) == 1 and noLeavingEdges(comp[0]):
                T.add(comp[0])

        return T


    def inEquality(self):
        q = -1
        rev = ~(self ** 2)

        new_delta = rev.d.copy()
        for a in rev.A:
            new_delta[(q, q), a] = set()
            for p in xproduct(self.F, (self.Q - self.F)):
                new_delta[(q, q), a].add(p)

        tmpQ = rev.Q.copy()
        tmpQ.add((q, q))

        tmpA = DFA((tmpQ, self.A, new_delta, (self.s, self.s), self.F))
        Z = set()
        witness = {}
        for state, word in tmpA.search((q, q), False):
            Z.add(state)
            witness[state] = word[1:][::-1]
        return Z, witness


class DFAr(DFA):
    """
    Should not constructed directly by the user.

    >>> d =  DFA("dea1.xml")
    >>> r =  ~d
    """
    #__slots__ =  ["_Q" , "_A" ,  "_d" ,  "_s" ,  "_F" ,  "_dea"]

    def __init__(self, dea):
        """
        Constructs the reverse dea from @dea.
         You should not need to call this directly.
         Consider the use of @~dea@ for generating the reverse dea.
        :param dea: DFA
        """
        self._Q = dea.Q
        self._A = dea.A
        self._s = dea.F
        self._F = {dea.s}

        self._d = dict()

        for q in dea.Q:
            for a in dea.A:
                p = dea.d[q, a]
                #print(" %s - %s ->%s" % (p , a , q))
                try:
                    self._d[p, a].add(q)
                except KeyError:
                    self._d[p, a] = {q}

        self._reachables = None

    def __invert__(self):
        return self._dea

