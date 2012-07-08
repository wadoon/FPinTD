# -*- encoding: utf-8 -*-
"""

"""

from dea import DEA, iterwords
#from itertools import

__author__ = "Alexander Weigl <weigla@fh-trier.de>"
__date__ = "2012-06-12"
__license__ = "gpl-3.0"


def reachable(dea, start, end, alphabet = None):
    """
    Wrapper around dea.search(…).

    It should be used when you want to check if @end is reachable form @start with an alphabet.
    If you do not need to specify an alphabet you should use dea.reachable(start,end) because
    it use pre calculated data.

    :param dea:
    :param start:
    :param end:
    :param alphabet:
    :return:
    """
    for q, w in dea.search(start, False, alphabet):
        if q == end:
            return w
    return False


def l12( dea ):
    """

    :param dea:
    :return:
    """

    A2 = dea ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in dea.F and f not in dea.F:
            for (state, z) in A2r.search((d, f), True): #with epsilon
                p, q = state
                w = dea.reachable(p, q)
                if w:
                    return {"w": w, "z": z[::-1], "+": d, "-": f, "p": p, "q": q}
    return {}


def b12( dea ):
    """

    :param dea:
    :return:
    """
    A2 = dea ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in dea.F and f not in dea.F:
            for (state, z) in A2r.search((d, f), True): #with epsilon
                p, q = state
                w = dea.reachable(p, q)
                if w:
                    v = A2.reachable((p, q), (p, q))
                    if v:
                        return {"w": w, "z": z[::-1], "+": d, "-": f, "p": p, "q": q, "v": v}
    return {}


def l1(dea ):
    """

    :param dea:
    :return:
    """
    return l1_1(dea), l1_2(dea)


def l1_1(dea ):
    """

    :param ea:
    :return:
    """
    A2 = dea ** 2
    A2r = A2.reverse
    # strongly connected components with witnesses in both direction
    Z, f, fr = A2.sCC()

    for r, t in A2.Q:
        if r in dea.F ^ t not in dea.F:
            for state, z in A2r.search((r, t), True):
                p, q = state
                if p in Z[q]:
                    w, v = f[p, q], fr[p, q]
                    return  {"w": w, "z": z, "r": r, "t": t, "p": p, "q": q, "v": v}
    return False


def l1_2(dea ):
    A2 = dea ** 2
    A3 = dea ** 3  # not implemented A2*A

    for (q, r, s) in A3.Q:
        for state1, u in A3.search((q, r, s), True):
            (q_, r_, s_) = state1
            if q_ == r_:
                for state, v in A3.search((q, q_, s_), True):
                    (q__, r__, s__) = state2
                    if q__ == s__ and r__ == r and s == s__:
                        for state3, z in A2.search((q_, s_)):
                            d, f = state3
                            if d in dea.F ^ f not in dea.F:
                                return {
                                    "w": w, "z": z, "v": v, "u": u,
                                    "q": q,
                                    "p": q_,
                                    "r": r,
                                    "s": s,
                                    "t:": s_,
                                    "d": d,
                                    "f": f
                                }
    return {}


def b1( dea ):
    A2 = dea ** 2
    A3 = dea ** 3
    Z, a, ar = dea.sCC()

    for q1, q5, q4 in A3.Q:
        for state1, u in A3.search((q1, q5, q4), True):
            q1_, q5_, q4_ = state1
            if q1_ == q5_:
                for q2 in Z(q1):
                    for state2, v in A3.search((q2, q1_, q4_), True):
                        q2_, q1__, q4__ = state2
                        if q2_ == q4 and q5 == q5__ and q4 == q4__:
                            w = A3.reachable((q1, q5, q4), (q1, q5, q4))
                            if w:
                                w_ = A3.reachable((q2, q5_, q4_), (q2, q5_, q4_))
                                if w_:
                                    for state3 in A2.search((q5_, q4_), True):
                                        d, f = state3
                                        if d in dea.F ^ f not in dea.F:
                                            return {
                                                "w": w, "z": z, "v": v, "u": u,
                                                "w_": w_,
                                                "y": a(q1, q2),
                                                "y_": ar(q1, q2),
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


def alpha(s ):
    return set(iterwords(s))


def l32( dea ):
    A2 = dea ** 2
    A2r = A2.reverse

    for (d, f) in A2.Q:
        if d in A2.F and f not in A2.F:
            for (state, z) in A2r.search((d, f), True): #with epsilon
                p, q = state
                v = A2.reachable(state)
                if v:
                    w = reachable(A2, p, q, alpha(v))
                    if w:
                        return {"w": w, "v": v, "z": z, "+": d, "-": f, "p": p, "q": q}
    return {}