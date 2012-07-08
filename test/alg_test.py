"""
Test cases for *dea* module.
"""

__author__ = 'weigla'
__date__ = '2012-06-16'

import sys, os, unittest
from  unittest import TestCase


sys.path.insert(0, os.path.abspath('../src/'))

import dea
from dea import *
import algorithms as alg
import witnesscheck as wc


class TestL12(TestCase):
    def setUp(self):
        self.deal12a = DEA("dea_test_l12_a.xml")
        self.deal12b = DEA("dea_test_l12_b.xml")
        self.deab12a = DEA("dea_test_b12_a.xml")
        self.deab12b = DEA("dea_test_b12_b.xml")
        self.deaUa  =  DEA("dea_test_unknown_a.xml")

        self.deal1_1na = DEA("dea_test_l1-1_n_a.xml")
        self.deal1_1nb = DEA("dea_test_l1-1_n_b.xml")
        self.deal1_2na = DEA("dea_test_l1-2_n_a.xml")

        self.deaBig = DEA("dea_python.xml")

    def assertPos(self, dea):
        w = alg.l12(dea)
        print("witness:", w)
        self.assertTrue(wc.checkWitnessL12(dea,w))
        self.assertTrue(len(w) > 0)

    def assertNeg(self, dea):
        w = alg.l12(dea)
        print("witness:", w)
        self.assertTrue(len(w) == 0)

    def test_positives(self):
        print("Test: b12_a")
        self.assertPos(self.deab12a)
        print("Test: b12_b")
        self.assertPos(self.deab12b)
        print("Test: l1-1 na")
        self.assertPos(self.deal1_1na)
        print("Test: l1-1 nb")
        self.assertPos(self.deal1_1nb)
        print("Test: l1-2 na")
        self.assertPos(self.deal1_2na)

    def test_negatives(self):
        print("Test: l12_a")
        self.assertNeg(self.deal12a)
        print("Test: l12_b")
        self.assertNeg(self.deal12b)


class TestB12(TestCase):
    def setUp(self):
        self.deal12a = DEA("dea_test_l12_a.xml")
        self.deal12b = DEA("dea_test_l12_b.xml")
        self.deab12a = DEA("dea_test_b12_a.xml")
        self.deab12b = DEA("dea_test_b12_b.xml")

        self.deal1_1na = DEA("dea_test_l1-1_n_a.xml")
        self.deal1_1nb = DEA("dea_test_l1-1_n_b.xml")
        self.deal1_2na = DEA("dea_test_l1-2_n_a.xml")

        self.deaUa  =  DEA("dea_test_unknown_a.xml")

    def assertPos(self, dea):
        w = alg.b12(dea)
        print("witness:", w)
        #        self.assertTrue(wc.checkWitnessL12(w))
        self.assertTrue(len(w) > 0)

    def assertNeg(self, dea):
        w = alg.b12(dea)
        print("witness:", w)
        self.assertTrue(len(w) == 0)

    def test_positives(self):
        print("Test: l1-1 na")
        self.assertPos(self.deal1_1na)
        print("Test: l1-1 nb")
        self.assertPos(self.deal1_1nb)
        print("Test: l1-2 na")
        self.assertPos(self.deal1_2na)

    def test_negatives(self):
        print("Test: l12_a")
        self.assertNeg(self.deal12a)
        print("Test: l12_b")
        self.assertNeg(self.deal12b)

        print("Test: b12_a")
        self.assertNeg(self.deab12a)
        print("Test: b12_b")
        self.assertNeg(self.deab12b)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDEA)
    unittest.TextTestRunner(verbosity=2).run(suite)
