__author__ = 'weigla'
__date__ = '2012-05-09'


import unittest, os, sys

sys.path.insert(0, os.path.join('../src'))

from graph import *
import trap

class TransitionGraphTest(unittest.TestCase):

    def setUp(self):
        self.deaSimpleTest = trap.load("DEA_TestSimple.xml")


    def test_init(self):
        tg = TransitionGraph(self.deaSimpleTest)
        self.checkTransitionGraphAgainstDEA(tg, self.deaSimpleTest)

    def checkTransitionGraphAgainstDEA(self, tg : TransitionGraph, dea):
        Q,A,delta,q0,F = dea

        for q in Q:
            for a in A:
                p = delta[q,a]
                r = tg._assoc[q][a]
                self.assertEqual(p,r, "Transition (%s,%s) should go to %s but goes to %s" % (q,a,p,r))


if __name__ == '__main__':
    unittest.main()
