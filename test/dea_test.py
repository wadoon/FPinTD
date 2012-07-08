"""
Test cases for *dea* module.
"""

__author__ = 'weigla'
__date__ = '2012-06-04'

import sys, os, unittest
from  unittest import TestCase


sys.path.insert(0, os.path.abspath('../src/'))

import dea
from dea import *


class TestDEA(TestCase):

    def setUp(self):
        self.dea1 = DEA("dea_test1.xml")
        self.dea1_2 = DEA("dea_test1_2.xml")
        self.dea1_3 = DEA("dea_test1_3.xml")

        self.dea2 = DEA("dea_test2.xml")
        self.dea2_2 = DEA("dea_test2_2.xml")
        self.dea2_3 = DEA("dea_test2_3.xml")

        self.deaBig = DEA("dea_python.xml")


        Q = { (x,y) for x in range(0,3) for y in range(0,3) }
        A = self.dea1.A

        d  = {}
        a,b="a","b"
        d[(0,0), a] = (2,2)
        d[(0,0), b] = (1,1)
        d[(0,1), a] = (2,2)
        d[(0,1), b] = (1,0)
        d[(0,2), a] = (2,0)
        d[(0,2), b] = (1,1)

        d[(1,0), a] = (2,2)
        d[(1,0), b] = (0,1)
        d[(1,1), a] = (2,2)
        d[(1,1), b] = (0,0)
        d[(1,2), a] = (2,0)
        d[(1,2), b] = (0,1)

        d[(2,0), a] = (0,2)
        d[(2,0), b] = (1,1)
        d[(2,1), a] = (0,2)
        d[(2,1), b] = (1,0)
        d[(2,2), a] = (0,0)
        d[(2,2), b] = (1,1)

        s = (0,0)
        F = set()

        self.dea1P = DEA([Q,A,d,s,F])


    def test_init(self):
        #test tuple assignment
        Q,A,d,s,F = self.dea1
        
        #test __str__
        self.assertTrue(type(str(self.dea1)) is str)

        #test __repr__
        self.assertTrue(type(repr(self.dea1)) is str)
        self.assertEqual(self.dea1, eval(repr(self.dea1)))

    def test_call2(self):
        #test normal behaviour
        self.assertTrue( self.deaBig(self.deaBig.s, "finally") \
                        == self.deaBig("finally") )
        self.assertTrue(self.deaBig("if|if") in self.deaBig.F)

        self.assertTrue( self.deaBig("while") == self.deaBig(
                self.deaBig(
                    self.deaBig(
                        self.deaBig(
                            self.deaBig("w"), "h"),"i"),"l"),"e"))

        self.assertTrue(self.deaBig( ["w", "h","i", "l", "e"]) == \
                        self.deaBig("while"))

        #test tuple behaviour
        a,b = self.deaBig(  (self.deaBig.s,self.deaBig.s) , "if|if")
        c   = self.deaBig("if|if")
        self.assertEqual((c,c),(a,b))
        self.assertTrue(a in self.deaBig.F)

        #get an exception
        with self.assertRaises(Exception):
            a,b = self.deaBig(  (10000,120202) , "def")

        #should not end up in an exception
        self.deaBig(  ('a','b') , "def", False)


    def test_productautomata(self):
        """
        test A**x
        """

        A_x = self.dea1 ** 3

        #invariant for each state (tuple and len of 3)
        stateInv = lambda q: type(q) is tuple and len(q) == 3

        #each state satisfies stateInv
        self.assertTrue( all( map( stateInv , A_x.Q)))        
        self.assertTrue(type(A_x.Q) is set)

        #alphabet stays the same
        self.assertTrue(A_x.A == self.dea1.A)
        
        #delta is totally defined for Q and A
        self.assertEqual( A_x.Q , {q for q,a in  A_x.d.keys()} )

        self.assertTrue( A_x.Q >= {q for q   in  A_x.d.values()} )
        self.assertEqual( A_x.A , {a for q,a in  A_x.d.keys()})
        self.assertEqual( len(A_x.Q) * len(A_x.A) , len(A_x.d) )

        self.assertTrue( stateInv(A_x.s) )

        self.assertEqual(self.dea1P, self.dea1**2)

        self.assertNotEqual(self.dea1, [])

       # self.assertEqual(self.dea1**2, self.dea1_2);
       # self.assertEqual(self.dea1**3, self.dea1_3);


    def test_eq(self):
        """
        test: A == B
        """
        Q,A,d,s,F = self.dea1
        
        self.assertTrue(self.dea1 == self.dea1)
        self.assertTrue(self.dea1 == [Q, A, d, s, F])
        self.assertTrue(self.dea1 == (Q, A, d, s, F))
        self.assertTrue(self.dea1 == DEA("dea_test1.xml"))

        self.assertTrue([Q, A, d, s, F] == self.dea1)
        self.assertTrue((Q, A, d, s, F) == self.dea1)
        self.assertTrue(DEA("dea_test1.xml")  == self.dea1)

        self.assertFalse(self.dea1 == [set(), A, d, s, F])
        self.assertFalse(self.dea1 == [Q, set() ,d ,s, F])
        self.assertFalse(self.dea1 == [Q, A, dict(), s, F])
        self.assertFalse(self.dea1 == [Q, A, d, None, F])
        self.assertFalse(self.dea1 == [Q, A, d, s, set()])                    


    def test_search(self): 
        pass

    def test_call1(self):
        Q,A,d,s,F = self.dea1

        for a in A:
            for q in Q: 
                p =  d[q , a]
                self.assertEqual(p , self.dea1(q , a))                        
    
    def test_invert(self): 
        idea =  ~ self.dea1

    def test_contains(self):
        self.assertTrue( 0 in self.dea1)
        self.assertTrue( 1 in self.dea1)
        self.assertTrue( 2 in self.dea1)
        self.assertFalse( 3 in self.dea1)

        self.assertTrue( (0,"a",2)   in self.dea1)
        self.assertTrue( (0,"b",1)   in self.dea1)
        self.assertTrue( (1,"a",2)   in self.dea1)

        self.assertFalse( (2,"a",2)   in self.dea1)


    def test_tarjan(self):
        Z1 = self.dea1.tarjan()
        self.assertEqual(Z1,{0: {0, 1, 2}, 1: {0, 1, 2}, 2: {0, 1, 2}})

        Z2 = self.dea2.tarjan()
        self.assertEqual(Z2,{0: {0, 1, 3, 4}, 1: {0, 1, 3, 4}, 2: {2}, 3: {0, 1, 3, 4}, 4: {0, 1, 3, 4}})

        Z3 = DEA("dea_test_b12_b.xml").tarjan()
        self.assertEqual(Z3,{0: {0, 1, 4}, 1: {0, 1, 4}, 2: {2}, 3: {3}, 4: {0, 1, 4}, 5: {5}})
        #p5,p2,p3
        #p1,p4,p0



    def test_sCC(self):
        Z,f,g = self.dea1.sCC()
        for comp1 in Z.values(): #fully mashed dea
            for comp2  in Z.values():
                self.assertEqual(comp1,comp2)

        self.assertEqual({0,1,2}, Z[0])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDEA)
    unittest.TextTestRunner(verbosity=2).run(suite)
