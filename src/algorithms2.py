# -*- encoding: utf-8 -*-
"""

"""

__author__ = "Alexander Weigl <weigla@fh-trier.de>"
__date__ = "2012-07-8"
__license__ = "gpl-3.0"

from dfa import tarjan2dict

def _calcW(dfa, states = None):
    """

    :param dfa:
    :return:
    """
    if states is None: 
        states = dfa.Q
    
    R = {}
    witness = {}
    for start in states:
        R[start] = set()
        witness[start] = {}
        for state,word in dfa.search(start):
            R[start].add(state)
            witness[start][state] = word

    return R,witness

def l12(dfa):
    """

    :param dfa:
    :return:
    """
    Z,witness_z = dfa.inEquality()
    R,witness_w = _calcW(dfa)

    for (p,q) in Z:
        if q in R[p]:
            w = witness_w[p][q]
            z = witness_z[(p,q)]
            return {'w':w, 'z': z, 'p':p, 'q':q}

    return {}

def b12(dfa):
    """

    :param dfa:
    :return:
    """
    A2 = (dfa ** 2)
    Z,witness_z = dfa.inEquality()
    R,witness_w = _calcW(dfa)
    T = A2.trivialComponents()

    for (p,q) in Z:
        if q in R[p] and (p,q) not in T:
            w = witness_w[p][q]
            z = witness_z[(p,q)]
            v = A2.reachable((p,q),(p,q))

            return {'w':w, 'z': z, 'p':p, 'q':q, 'v': v}

    return {}

def l1(dfa):
    return l1_1(dfa), l1_2(dfa)

def l1_1(dfa):
    Z,witness_z = dfa.inEquality()
    ZK = tarjan2dict(dfa.tarjan())
    R,witness_wv = _calcW(dfa)
    for (p,q) in Z:
        if q in ZK[p]:
            w = witness_wv[p][q]
            v = witness_wv[q][p]
            z = witness_z[(p,q)]
            return {'w':w, 'z': z,'v':v, 'p':p, 'q':q}

    return {}

def l1_2(dfa):
    #A2 = dfa ** 2
    A3 = dfa ** 3  # not implemented A2*A
    Z, witness_z = dfa.inEquality()

    for (q, r, s) in A3.Q:
        for (q_, r_, s_), u in A3.search((q, r, s), True):
            if q_ == r_:
                for (q__, r__, s__), v in A3.search((q, q_, s_), True):
                    if q__ == s__ and r__ == r and s == s__:
                        if (q_,s_) in Z or (s_,q_) in Z:
                            z = witness_z[(q_,s_)] if ((q_,s_) in Z) \
                                                 else witness_z[(s_,q_)]

                            return {
                                "z": z, "v": v, "u": u,
                                "q": q,
                                "p": q_,
                                "r": r,
                                "s": s,
                                "t": s_,
                                "d": dfa(q_, z),
                                "f": dfa(s_, z)
                            }
    return {}

def b1(dfa):
    """

    :param dfa:
    :return:
    """
    #A2 = dfa ** 2
    A3 = dfa ** 3
    ZK = tarjan2dict(dfa.tarjan())
    Z, witness_z = dfa.inEquality()
    T = A3.trivialComponents()

    for q1, q5, q4 in A3.Q:
        for (q1_, q5_, q4_), u in A3.search((q1, q5, q4), True):
            if q1_ == q5_:
                for q2 in ZK[q1]:
                    for (q2_, q1__, q4__), v in A3.search((q2, q1_, q4_), True):
                        if q2_ == q4 and q5 == q1__ and q4 == q4__:
                            if      (q1,q5,q4) not in T    \
                                and (q2,q5_,q4_) not in T  \
                                and ((q5_,q4_) in Z or (q4_,q5_) in Z):

                                witness = A3.reachable((q1, q5, q4), (q1, q5, q4))
                                w_ = A3.reachable((q2, q5_, q4_), (q2, q5_, q4_))

                                z = witness_z[(q5_,q4_)] if ((q5_,q4_) in Z)\
                                                     else witness_z[(q4_,q5_)]

                                return {
                                    "w": witness, "z": z, "v": v, "u": u,
                                    "w'": w_,
                                    "y": dfa.reachable(q1, q2),
                                    "y'": dfa.reachable(q2, q1),
                                    "q1": q1,
                                    "q2": q2,
                                    "q3": q5_,
                                    "q4": q4,
                                    "q5": q5,
                                    "q6": q4_,
                                    "d": dfa(q5_,z),
                                    "f": dfa(q4_,z)
                                }
    return {}



def l32(dfa):
    """
    
    """
    def _calcAlphaComp(A, K):
        alpha = set()
        
        for (s,a),e in A.d.items():
            if s in K and e in K:
                alpha.add(a)
                
        return alpha
    
    def _witness_v(K, q):
        def _removeEdge(state , word):
            prev = state
            nxt = state
            
            for symbol in word:
                nxt = dfa(prev,symbol)                
                visited.add( ( prev, nxt, symbol )  )                
                prev = nxt
                        
        E = set()
        for (s,a),e in A2.d.items():
            if s in K and e in K:
                E.add( (s,e,a) )
        
        
        R,paths = _calcW(A2,K)
        witness = ""
        visited = set()

        for (start,end, a) in E:
            if (start,end,a) not in visited:
                w = paths[q][start]
                v = paths[end][q]
            
                visited.add((start,end,a))
                _removeEdge(start, witness)
                _removeEdge(end, v)
                
                witness += w+a+v
                
                #loop invariants
                #assert visited <= E
                assert A2(q,witness)==q
                
                #our witness is satisfied with all symbols
                if alpha_v[q] == set(witness): break

        return witness
    
    A2 = dfa ** 2
    ZK = A2.tarjan() 
    Z,witness_z = dfa.inEquality()
    
    alpha_v = {}
    
    for K in ZK:
        alpha = _calcAlphaComp(A2, K)
        for q in K:
            alpha_v[q] = alpha
            
    _witness_z = lambda a,b : witness_z[a,b] \
                              if   (a,b) in witness_z \
                              else witness_z[b,a]
    ZK = tarjan2dict(ZK)
    
    for p,q in A2.Q:
        if (p,q) in Z or (q,p) in Z:
            witness_w = dfa.reachable(p,q, False, alpha_v[(p,q)])
            if witness_w:
                z = _witness_z(p,q)
                v = _witness_v(ZK[(p,q)], (p,q))
                return {"z" : z, "w": witness_w, "v": v, "p":p, "q":q}
    return {}
    

