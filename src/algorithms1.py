# -*- encoding: utf-8 -*-
"""

"""
__author__ = "Alexander Weigl <weigla@fh-trier.de>"
__date__ = "2012-06-12"
__license__ = "gpl-3.0"

from dfa import iterwords


def l12( dfa ):
    """

    :param dfa:
    :return:
    """

    A2 = dfa ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in dfa.F and f not in dfa.F:
            for ((p,q), z) in A2r.search((d, f), True): #with epsilon
                witness = dfa.reachable(p, q)
                if witness:
                    return {"w": witness, "z": z[::-1], "+": d, "-": f, "p": p, "q": q}
    return {}

def b12( dfa ):
    """

    :param dfa:
    :return:
    """
    A2 = dfa ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in dfa.F and f not in dfa.F:
            for ((p,q), z) in A2r.search((d, f), True): #with epsilon
                witness = dfa.reachable(p, q)
                if witness:
                    v = A2.reachable((p, q), (p, q))
                    if v:
                        return {"w": witness, "z": z[::-1], "+": d, "-": f, "p": p, "q": q, "v": v}
    return {}

def l1(dfa ):
    """

    :param dfa:
    :return:
    """
    return l1_1(dfa), l1_2(dfa)

def l1_1(dfa ):
    """

    :param ea:
    :return:
    """
    A2 = dfa ** 2
    A2r = A2.reverse
    # strongly connected components with witnesses in both direction
    Z, witness_w, witness_v = dfa.sCC()

    for r, t in A2.Q:
        if (r in dfa.F) ^ (t in dfa.F):
            for (p,q), z in A2r.search((r, t), True):
                if p in Z[q]:
                    #if p == q: continue
                    witness, v = witness_w[p, q], witness_v[p,q]
                    return  {"w": witness, "z": z[::-1], "r": r, "t": t, "p": p, "q": q, "v": v}
    return False

def l1_2(dfa ):
    A2 = dfa ** 2
    A3 = dfa ** 3  # not implemented A2*A

    for (q, r, s) in A3.Q:
        for (q_, r_, s_), u in A3.search((q, r, s), True):
            if q_ == r_:
                for  (q__, r__, s__), v in A3.search((q, q_, s_), True):
                    if q__ == s__ and r__ == r and s == s__:
                        for (d,f), z in A2.search((q_, s_)):
                            if (d in dfa.F) ^ (f in dfa.F):
                                return {
                                    "z": z, "v": v, "u": u,
                                    "q": q,
                                    "p": q_,
                                    "r": r,
                                    "s": s,
                                    "t": s_,
                                    "d": d,
                                    "f": f
                                }
    return {}

def b1(dfa):
    A2 = dfa ** 2
    A3 = dfa ** 3
    Z, a, ar = dfa.sCC()

    for q1, q5, q4 in A3.Q:
        for (q1_, q5_, q4_), u in A3.search((q1, q5, q4), True):
            if q1_ == q5_:
                for q2 in Z[q1]:
                    for (q2_, q1__, q4__), v in A3.search((q2, q1_, q4_), True):
                        if q2_ == q4 and q5 == q1__ and q4 == q4__:
                            witness = A3.reachable((q1, q5, q4), (q1, q5, q4))
                            if witness:
                                w_ = A3.reachable((q2, q5_, q4_), (q2, q5_, q4_))
                                if w_:
                                    for (d,f),z in A2.search((q5_, q4_), True):
                                        if (d in dfa.F) ^ (f in dfa.F):
                                            return {
                                                "w": witness, "z": z, "v": v, "u": u,
                                                "w'": w_,
                                                "y": a[q1, q2],
                                                "y'": ar[q1, q2],
                                                "q1": q1,
                                                "q2": q2,
                                                "q3": q5_,
                                                "q4": q4,
                                                "q5": q5,
                                                "q6": q4_,
                                                "d": d,
                                                "f": f
                                            }
    return {}


def alpha(s):
    return set(iterwords(s))

def l32( dfa ):
    A2 = dfa ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in A2.F and f not in A2.F:
            for ((p,q), z) in A2r.search((d, f), True): #with epsilon
                v = A2.reachable((p,q),(p,q))
                if v:
                    witness = dfa.reachable(p, q, alpha(v))
                    if witness:
                        return {"w": witness, "v": v, "z": z, "+": d, "-": f, "p": p, "q": q}
    return {}