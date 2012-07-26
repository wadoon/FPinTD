__author__ = 'weigla'


import sys, os, dfa

sys.path.insert(0, os.path.abspath('../src/'))

if __name__ == "__main__":

    dea = dfa.DFA("dea_test2.xml")

    for k, v in dea.d.items():
        a, b = k;
        print("delta(%s,%s,%s)." % (a, v, b))

    print("start(%s)." % dea.s)

    for q in dea.F:
        print("accept(%s)." % q)

    for q in (dea.Q - dea.F):
        print("notaccept(%s)." % q)

#    dea.todot()
