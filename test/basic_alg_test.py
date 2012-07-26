"""
Test cases for *dea* module.
"""
from __future__ import print_function
from __future__ import division


__author__ = 'weigla'
__date__ = '2012-06-16'


import sys, os
import unittest

sys.path.insert(0, os.path.abspath('../src/'))

import algorithms1
from dfa import DFA, valid_witness
import witnesscheck as wc
import algorithms1 as a1
import algorithms2 as a2


deal12a = DFA("dea_test_l12_a.xml")
deal12b = DFA("dea_test_l12_b.xml")
deab12a = DFA("dea_test_b12_a.xml")
deab12b = DFA("dea_test_b12_b.xml")
deaUa = DFA("dea_test_unknown_a.xml")

deal1_1na = DFA("dea_test_l1-1_n_a.xml")
deal1_1nb = DFA("dea_test_l1-1_n_b.xml")
deal1_2na = DFA("dea_test_l1-2_n_a.xml")
deab1_na = DFA("dea_test_b1_n_a.xml")
deab1_nb = DFA("dea_test_b1_n_b.xml")

deaBig = DFA("dea_python.xml")

dea_s1_l12_1 = DFA("dea_test_series1_l12_1.xml")
dea_s1_l12_2 = DFA("dea_test_series1_l12_2.xml")
dea_s1_l12_3 = DFA("dea_test_series1_l12_3.xml")
dea_s1_l12_4 = DFA("dea_test_series1_l12_4.xml")
dea_s1_l1_1 = DFA("dea_test_series1_l1_1.xml")
dea_s1_l1_2 = DFA("dea_test_series1_l1_2.xml")
dea_s1_l32_1 = DFA("dea_test_series1_l32_1.xml")

deal32_na = DFA("dea_test_l32_na.xml")
deal32_nb = DFA("dea_test_l32_nb.xml")
deal32_nc = DFA("dea_test_l32_nc.xml")



L12, B12, L1, B1, L32 = range(5)

ALGO_NAMES = "l12 b12 l1 b1 l32".split(" ") 

checker = {
            L12 : wc.CHECKERS['l12'],
            B12 : wc.CHECKERS['b12'],
            L1: wc.CHECKERS['l1'],
            B1: wc.CHECKERS['b1'],
            L32: wc.CHECKERS['l32'],
}


automata = [
            (deal12a, {L12,B12,L1,B1,L32}),
            (deal12b, {L12,B12,L1,B1,L32}),
            (deab12a, {B12,L1,B1,L32}),
            (deab12b, {B12,B1,L32}),
            (deal1_1na, {}),
            (deal1_1nb, {}),
            (deal1_2na, {}),
            (deab1_na,  {}),
            (deab1_nb,  {}),
            (dea_s1_l12_1, {L12,B12,L1,B1,L32}),
            (dea_s1_l12_2, {L12,B12,L1,B1,L32}),
            (dea_s1_l12_3, {L1,B1,L32}),
            (dea_s1_l12_4, {L1,B1,L32}),
            (dea_s1_l1_1, {L1,B1,L32}),
            (dea_s1_l1_2, {L1,B1,L32}),
            (dea_s1_l32_1, {L1, B1, L32}),
            (deal32_nc, {}),   
            (deal32_na, {}),    
            (deal32_nb, {}),
            #(deaBig, level(B12)) #bad decision for testing
]



class TestAlgorithmTest(unittest.TestCase):
    def test_automat(self):
        for num,(dea, levels) in enumerate(automata):
            print("Checking [%s]" % dea.filename, end=": ")
            for level in range(L32+1):
                expected = level not in levels
                self.assertAlgorithm(a1 , level , expected , dea, num)
                self.assertAlgorithm(a2 , level , expected , dea, num)
            print("\n")
            
    def assertAlgorithm(self, module, level, expected, dea, number):
        algo = ALGO_NAMES[level]
        
        #call algorithm
        witness = getattr(module, algo)(dea)
        
        msg1 = "#%d,%s: Witness should be equal to %s but was %s %s" % \
               (number,algo, expected, valid_witness(witness), witness)        
                
                                 
        if valid_witness(witness):
            try:
                check = checker[level]
                t = check(dea, witness)
                print(" -%s " % algo , end="")
            except Exception as e:
                msg2 = "#%d: Witness %s rejected by checker for %s" % \
                            (number, witness, algo)
#                raise AssertionError(msg2) from e
                raise AssertionError(msg2,e)
        else:
            print(" +%s " % algo , end="")
            
        if not (level == L32 and module == algorithms1):
            self.assertEqual(expected, valid_witness(witness), msg1);
            
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAlgorithmTest))
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    
