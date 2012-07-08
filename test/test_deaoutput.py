__author__ = 'weigla'



if __name__ == "__main__":
    import sys, os, unittest
    from  unittest import TestCase

    sys.path.insert(0, os.path.abspath('../src/'))

    import dea
    from dea import *

    dea = DEA("dea_test2.xml")

    for k,v in dea.d.items():
	a,b = k
        print("delta(%s,%s,%s)." % (a,v,b))

    print("start(%s)." % dea.s)

    for q in dea.F:
        print("accept(%s)." % q)
	
    for q in (dea.Q - dea.F):
	print("notaccept(%s)."%q)

#    dea.todot()
