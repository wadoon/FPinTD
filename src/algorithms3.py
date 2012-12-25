# -*- encoding: utf-8 -*-
"""

"""

__author__ = "Alexander Weigl <Alexander.Weigl@student.kit.edu>"
__date__ = "2012-12-07"
__license__ = "gpl-3.0"

from itertools import starmap
from dfa import DFA

def first(*a):
    return a[0]


def R(dfa, n, mode='R', filter_func=None):
    """
    :param dfa:
    :param n:
    :return:
    """

    dfa = dfa ** n
    temp = {start: starmap(first, dfa.search(start))
            for start in dfa.Q}

    if mode == 'D':
        return temp
    else:
        ret = {(s, e)
               for s in temp
               for e in temp[s]}
        return ret


def Z(dfa):
    Z, w = dfa.inEquality()
    return Z


def L(dfa, n):
    pa = dfa ** n
    T = pa.trivialComponents()
    return pa.Q - T


def P(dfa, n):
    pa = dfa ** n
    scc = pa.tarjan()
    return scc,


def Pf(dfa, n):
    scc = P(dfa, n)
    return {state: K
            for K in scc
            for state in K}


def l12(dfa):
    return len(Z(dfa) & R(dfa, 1)) > 0


def b12(dfa):
    return len(Z(dfa) & R(dfa, 1) & L(dfa, 2)) > 0


def l1_1(dfa):
    scc = Pf(dfa, 1)
    for (p, q) in Z(dfa):
        if p in scc[q]:
            return True
    return False


def l1_2(dfa):
    _R = R(dfa, 3, 'R')
    for (q, r, s), (p, p_, t) in _R:
        if p == p_ and p != s and ((q, p, t), (s, r, s)) in _R:
            return True
    return False


def b1(dfa):
    _R = R(dfa, 3)
    _L = L(dfa, 3)
    _P = Pf(dfa, 1)

    #for (q1, q5, q4 ), (q3, q3, q6 ) in _R:
    for (a, b, c ), (d, e, f ) in _R:
        if d == e:
            q1, q2, q3, q4, q5, q6 = a, 0, d, c, b, f
            #   ((q2, q3, q6 ), (q4, q5, q4 )) _R:
            for ((g, h, i ), (j, k, l )) in _R:
                q2 = g
                if q3 == h and q6 == i and q4 == j == l and q5 == k:
                    c1 = q1 in _P[q2]
                    c2 = (q1, q5, q4 ) in _L
                    c3 = (q2, q3, q6 ) in _L
                    c4 = q3 == q6
                    if all((c1, c2, c3, c4)):
                        return True
    return False


def _calcAlphaComp(dfa, K):
    alpha = {a for (s, a), e in dfa.d.items()
             if s in K and e in K}
    return alpha


def l32(dfa):
    """

    :param dfa:
    :return:
    """
    A2 = dfa ** 2

    alpha_v = dict()
    for K in P(dfa, 2):
        alpha = _calcAlphaComp(A2, K)
        for q in K:
            alpha_v[q] = alpha

    _Z = Z(dfa)
    for p, q in A2.Q:
        if (p, q) in _Z or (q, p) in _Z:
            if dfa.reachable(p, q, False, alpha_v[(p, q)]):
                return True
    return False


class uvGraph(object):
    V_EDGE, U_EDGE = 0, 1

    def __init__(self, dfa: DFA):
        self.dfa = dfa
        self.nodes = set()
        self.edges_u = dict()
        self.edges_v = dict()

        dfa3 = dfa ** 3
        _L3 = L(dfa3, 1)
        _L5 = L(dfa, 5)

        for q in dfa3.Q:
            if q in _L3:
                self.nodes.add(q)

        def insert(ds, k, v):
            try:
                ds[k].add(v)
            except KeyError:
                ds[k] = {v}

        for v1 in self.nodes:
            for v2 in self.nodes:
                if dfa3.reachable(v1, v2):
                    insert(self.edges_u, v1, v2)

        for (a, b, c), (d, e, f) in R(dfa3, 1):
            if a == d:
                r, s, t, s_, t_ = a, b, c, e, f
                if (r, s, t, s, t ) in _L5:
                    v1 = (r, s, t)
                    v2 = (r, s_, t_)
                    insert(self.edges_v, v1, v2)


    def succ(self, node, type):
        if type == uvGraph.V_EDGE:
            return self.edges_v[node]
        else:
            return self.edges_u[node]


    def search(self, start):
        queue = [(start, uvGraph.V_EDGE)]
        path = {start: []}
        uv_paths = set()
        reached = set()

        while len(queue) > 0:
            current, edgeType = queue.pop(0)
            nextEdgeType = 1 - edgeType
            for new in self.succ(current, edgeType):
                if (new, nextEdgeType) not in reached:
                    reached.add((new, nextEdgeType))
                    path[new, nextEdgeType] = path((current, nextEdgeType)) + (new, nextEdgeType)
                    if nextEdgeType == uvGraph.V_EDGE:
                        uv_paths.add(path[new, nextEdgeType])
                    queue.add((new, nextEdgeType))
        return uv_paths


def b32(dfa: DFA):
    _R = R(dfa, 2)
    _Z = Z(dfa)
    _uvG = uvGraph(dfa)
    _L = L(dfa, 2)

    dfa2 = dfa ** 2

    for s1, s2 in dfa2.Q:
        if (s1, s2 ) in _Z and (s1, s2) in _L and (s1, s2) in _R:
            if (s2, s1, s2 ) in _uvG.search((s1, s1, s2 )):
                return True
    return False



