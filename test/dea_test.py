"""
Test cases for *dea* module.
"""

__author__ = 'weigla'
__date__ = '2012-06-04'

import sys, os, unittest
from  unittest import TestCase


sys.path.insert(0, os.path.abspath('../src/'))

import dfa
from dfa import *


class TestDEA(TestCase):

    def setUp(self):
        self.dea1 = DFA("dea_test1.xml")
        self.dea1_2 = DFA("dea_test1_2.xml")
        self.dea1_3 = DFA("dea_test1_3.xml")

        self.dea2 = DFA("dea_test2.xml")
        self.dea2_2 = DFA("dea_test2_2.xml")
        self.dea2_3 = DFA("dea_test2_3.xml")

        self.deaBig = DFA("dea_python.xml")


        Q = { (x, y) for x in range(0, 3) for y in range(0, 3) }
        A = self.dea1.A

        d = {}
        a, b = "a", "b"
        d[(0, 0), a] = (2, 2)
        d[(0, 0), b] = (1, 1)
        d[(0, 1), a] = (2, 2)
        d[(0, 1), b] = (1, 0)
        d[(0, 2), a] = (2, 0)
        d[(0, 2), b] = (1, 1)

        d[(1, 0), a] = (2, 2)
        d[(1, 0), b] = (0, 1)
        d[(1, 1), a] = (2, 2)
        d[(1, 1), b] = (0, 0)
        d[(1, 2), a] = (2, 0)
        d[(1, 2), b] = (0, 1)

        d[(2, 0), a] = (0, 2)
        d[(2, 0), b] = (1, 1)
        d[(2, 1), a] = (0, 2)
        d[(2, 1), b] = (1, 0)
        d[(2, 2), a] = (0, 0)
        d[(2, 2), b] = (1, 1)

        s = (0, 0)
        F = set()

        self.dea1P = DFA([Q, A, d, s, F])


    def test_init(self):
        #test tuple assignment
        Q, A, d, s, F = self.dea1
        
        #test __str__
        self.assertTrue(type(str(self.dea1)) is str)

        #test __repr__
        self.assertTrue(type(repr(self.dea1)) is str)
        self.assertEqual(self.dea1, eval(repr(self.dea1)))

    def test_call2(self):
        #test normal behaviour
        self.assertTrue(self.deaBig(self.deaBig.s, "finally") \
                        == self.deaBig("finally"))
        self.assertTrue(self.deaBig("if|if") in self.deaBig.F)

        self.assertTrue(self.deaBig("while") == self.deaBig(
                self.deaBig(
                    self.deaBig(
                        self.deaBig(
                            self.deaBig("w"), "h"), "i"), "l"), "e"))

        self.assertTrue(self.deaBig(["w", "h", "i", "l", "e"]) == \
                        self.deaBig("while"))

        #test tuple behaviour
        a, b = self.deaBig((self.deaBig.s, self.deaBig.s) , "if|if")
        c = self.deaBig("if|if")
        self.assertEqual((c, c), (a, b))
        self.assertTrue(a in self.deaBig.F)

        #get an exception
        with self.assertRaises(Exception):
            a, b = self.deaBig((10000, 120202) , "def")

        #should not end up in an exception
        self.deaBig(('a', 'b') , "def", False)


    def test_productautomata(self):
        """
        test A**x
        """

        A_x = self.dea1 ** 3

        #invariant for each state (tuple and len of 3)
        stateInv = lambda q: type(q) is tuple and len(q) == 3

        #each state satisfies stateInv
        self.assertTrue(all(map(stateInv , A_x.Q)))        
        self.assertTrue(type(A_x.Q) is set)

        #alphabet stays the same
        self.assertTrue(A_x.A == self.dea1.A)
        
        #delta is totally defined for Q and A
        self.assertEqual(A_x.Q , {q for q, a in  A_x.d.keys()})

        self.assertTrue(A_x.Q >= {q for q   in  A_x.d.values()})
        self.assertEqual(A_x.A , {a for q, a in  A_x.d.keys()})
        self.assertEqual(len(A_x.Q) * len(A_x.A) , len(A_x.d))

        self.assertTrue(stateInv(A_x.s))

        self.assertEqual(self.dea1P, self.dea1 ** 2)

        self.assertNotEqual(self.dea1, [])

       # self.assertEqual(self.dea1**2, self.dea1_2);
       # self.assertEqual(self.dea1**3, self.dea1_3);


    def test_eq(self):
        """
        test: A == B
        """
        Q, A, d, s, F = self.dea1
        
        self.assertTrue(self.dea1 == self.dea1)
        self.assertTrue(self.dea1 == [Q, A, d, s, F])
        self.assertTrue(self.dea1 == (Q, A, d, s, F))
        self.assertTrue(self.dea1 == DFA("dea_test1.xml"))

        self.assertTrue([Q, A, d, s, F] == self.dea1)
        self.assertTrue((Q, A, d, s, F) == self.dea1)
        self.assertTrue(DFA("dea_test1.xml") == self.dea1)

        self.assertFalse(self.dea1 == [set(), A, d, s, F])
        self.assertFalse(self.dea1 == [Q, set() , d , s, F])
        self.assertFalse(self.dea1 == [Q, A, dict(), s, F])
        self.assertFalse(self.dea1 == [Q, A, d, None, F])
        self.assertFalse(self.dea1 == [Q, A, d, s, set()])                    


    def test_search(self): 
        L = list(self.dea2.search(self.dea2.s, True))
        self.assertEqual([(1, ''), (0, 'a'), (2, 'b'), (4, 'ab'), (1, 'aba'), (3, 'abb')], L)

        L = list(self.dea1.search(self.dea1.s, True))
        self.assertEqual([(0, ''), (2, 'a'), (1, 'b'), (0, 'aa')], L)
        
        L = list(self.deaBig.search(self.deaBig.s, True))
        print(set(L))
        self.assertEqual({(2, 'retu'), (3, 'an'), (49, 'if|'), (8, 'y'), (13, 'exe'), (49, ''), (60, 'yi'), (15, 'yie'), (11, 'eli'), (32, 'tr'), (18, 'f'), (30, 'fin'), (66, 'br'), (67, 'lamb'), (4, 'glob'), (53, 'cl'), (55, 'fi'), (41, 'bre'), (68, 'im'), (63, 'la'), (45, 'brea'), (62, 'h'), (19, 'p'), (71, 'els'), (65, 'as'), (12, 'cont'), (14, 'exc'), (44, 'pri'), (16, 'glo'), (61, 'gl'), (70, 'exce'), (46, 'imp'), (50, 'wh'), (27, 'o'), (39, 'retur'), (56, 'asse'), (26, 'b'), (7, 'g'), (29, 'con'), (24, 'd'), (58, 'ex'), (52, 'de'), (69, 'lambd'), (17, 'c'), (25, 'a'), (64, 'pr'), (22, 'i'), (6, 'w'), (57, 'fr'), (20, 'n'), (9, 'r'), (23, 'fina'), (35, 'ret'), (1, 'pas'), (48, 're'), (31, 'fro'), (5, 'e'), (59, 'el'), (43, 'final'), (34, 'if'), (38, 'globa'), (40, 'ass'), (42, 'conti'), (0, 'no'), (47, 'lam'), (54, 'co'), (10, 't'), (37, 'rai'), (33, 'contin'), (36, 'whi'), (51, 'ra'), (21, 'l'), (28, 'pa')},set(L))

    def test_reachable(self):
        self.assertEquals(self.dea1.reachable(0, 1), "b")
        self.assertTrue(self.dea1.reachable(0, 0) in ("aa", "bb"))
        self.assertEquals(self.dea1.reachable(0, 2), "a")
        
        self.assertEqual(self.dea2.reachable(1, 2), "b")
        self.assertEqual(self.dea2.reachable(1, 0), "a")
        self.assertEqual(self.dea2.reachable(0, 1), "ba")
        self.assertTrue(self.dea2.reachable(0, 0) in ("baa","bba"))
        self.assertEqual(self.dea2.reachable(0, 4), "b")
        self.assertTrue(self.dea2.reachable(4, 2) in ("bb","ab"))

        self.assertEqual(self.dea2.reachable(2, 1), False)
        self.assertEqual(self.dea2.reachable(2, 0), False)
        self.assertEqual(self.dea2.reachable(2, 3), False)
        self.assertEqual(self.dea2.reachable(2, 4), False)
        self.assertEqual(self.dea2.reachable(2, 5), False)
        
        self.assertTrue(self.dea2.reachable(2, 2) in ("b", "a"))
    
    
        test = ~self.dea2
        
        self.assertEqual(test.reachable(0, 1), "a")
        self.assertEqual(test.reachable(1, 4), "a")
        self.assertEqual(test.reachable(2, 1), "ab")
        self.assertEqual(test.reachable(2, 3), "ab")
        self.assertEqual(test.reachable(3, 4), "b")
        self.assertEqual(test.reachable(0, 3), "a")
        self.assertEqual(test.reachable(0, 1), "a")
        self.assertEqual(test.reachable(2, 0), "a")
        
    
    def test_call1(self):
        Q, A, d, s, F = self.dea1

        for a in A:
            for q in Q: 
                p = d[q , a]
                self.assertEqual(p , self.dea1(q , a))                        
    
    def test_invert(self): 
        idea = ~self.dea1

    def test_contains(self):
        self.assertTrue(0 in self.dea1)
        self.assertTrue(1 in self.dea1)
        self.assertTrue(2 in self.dea1)
        self.assertFalse(3 in self.dea1)

        self.assertTrue((0, "a", 2)   in self.dea1)
        self.assertTrue((0, "b", 1)   in self.dea1)
        self.assertTrue((1, "a", 2)   in self.dea1)

        self.assertFalse((2, "a", 2)   in self.dea1)


    def test_tarjan(self):
        Z1 = self.dea1.tarjan()
        self.assertEqual(Z1, [(0, 1, 2)])
        self.assertEqual(tarjan2dict(Z1),
                         {0: {0, 1, 2}, 1: {0, 1, 2}, 2: {0, 1, 2}})

        Z2 = self.dea2.tarjan()
        #self.assertEqual(Z2,[(0,)]
        self.assertEqual(tarjan2dict(Z2),
                         {0: {0, 1, 3, 4}, 1: {0, 1, 3, 4}, 2: {2}, 3: {0, 1, 3, 4}, 4: {0, 1, 3, 4}})

        Z3 = DFA("dea_test_b12_b.xml").tarjan()
        self.assertEqual(tarjan2dict(Z3),
                         {0: {0, 1, 4}, 1: {0, 1, 4}, 2: {2}, 3: {3}, 4: {0, 1, 4}, 5: {5}})


    def test_sCC(self):
        Z, f, g = self.dea1.sCC()
        for comp1 in Z.values(): #fully mashed dea
            for comp2  in Z.values():
                self.assertEqual(comp1, comp2)
        self.assertEqual({0, 1, 2}, Z[0])

        Z, f, g = self.dea2.sCC()
        for comp1 in Z.values(): #fully mashed dea
            for comp2  in comp1:
                self.assertEqual(Z[comp2], comp1)
        for q in self.dea2.Q:
            self.assertTrue(Z[q])            
        self.assertEqual({0, 1, 3, 4}, Z[0])
        self.assertEqual({2}, Z[2])


    def test_inEquality(self):
        def check_delta(dea, witness):
            return all((dea(p,word) in dea.F and dea(q,word) not in dea.F 
                            for (p,q),word in witness.items()))
        
        Z, witness = self.dea1.inEquality()
        self.assertEqual((Z, witness),
                         ({(1, 2), (0, 1), (1, 0), (2, 1)},
                          {(1, 2): '', (0, 1): 'b', (1, 0): '', (2, 1): 'b'}))
        self.assertTrue(check_delta(self.dea1,witness))
        
        Z, witness = self.dea2.inEquality()
        self.assertEqual((Z,witness),
                       ({(0, 1), (1, 2), (3, 2), (3, 0), (4, 1), (3, 1), (1, 4),
                         (4, 3), (0, 4), (1, 0), (4, 2), (0, 3), (3, 4), (0, 2), (4, 0)},
                         {(0, 1): 'bb', (1, 2): 'abb', (3, 2): '', (3, 0): '', (4, 1): 'b', (3, 1): '',
                          (1, 4): 'abb', (4, 3): 'b', (0, 4): 'bb', (1, 0): 'abb', (4, 2): 'b',
                          (0, 3): 'bb', (3, 4): '', (0, 2): 'bb', (4, 0): 'b'}))
        self.assertTrue(check_delta(self.dea2,witness))

        deab12a = DFA("dea_test_b12_a.xml")
        Z,witness = deab12a.inEquality()
        self.assertEqual(Z, {(0, 1), (1, 2), (3, 2), (1, 3), (0, 3), (0, 2)})
        self.assertTrue(check_delta(deab12a, witness))

    def test_trivialComponents(self):
        T = self.dea1.trivialComponents()
        self.assertEqual(T, set())
        T = self.dea2.trivialComponents()
        self.assertEqual(T, set())
        T = self.deaBig.trivialComponents()
        self.assertEqual(T, set())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDEA)
    unittest.TextTestRunner(verbosity=2).run(suite)
