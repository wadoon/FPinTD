# -*- encoding: utf-8 -*-
"""

"""

__author__ = "Alexander Weigl <Alexander.Weigl@student.kit.edu>"
__date__ = "2012-12-07"
__license__ = "gpl-3.0"

from itertools import starmap


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
    pass


def l32(dfa):
    pass


def b32(dfa):
    pass



