#!/usr/bin/python3
'''
Created on 12.07.2012

@author: weigla
'''

from optparse import OptionParser
from pprint import pprint

import dfa


KNOWN_ALGORITHMS = ["l12", "b12", "l1", "b1", "l32"]
alg = None


def createOptionParser():
    opt = OptionParser(usage="",
                       version="",
                       description="",
                       epilog="");

    opt.add_option("-c", "--classes", action="store", default=False, help="Test only for given classes")
    opt.add_option("-w", "--witnesses", action="store_true", help="Print the witnesses")
    opt.add_option("-v", "--verify-wintnesses", action="store_true", help="check the witnesses for correctness")
    opt.add_option("-m", "--module", action="store", help="1 or 2 for the algo module", default="algorithms2")

    return opt


def run(module, algname, dea):
    return getattr(module, algname)(dea)

if __name__ == '__main__':
    o = createOptionParser()
    args, files = o.parse_args()

    if args.classes:
        algorithms = set(args.classes)
    else:
        algorithms = KNOWN_ALGORITHMS

    print_witnesses = args.witnesses
    verify_wintesses = args.witnesses

    alg_module = __import__(args.module)

    for fil in files:
        dea = dfa.DFA(fil)
        for algorithm in algorithms:
            witness = run(alg_module, algorithm, dea)
            if dfa.valid_witness(witness):
                print("File: %s ∉ %s" % (fil, algorithm))
                if print_witnesses:
                    print(" " * 4, end="")
                    pprint(witness, indent=4)
                if verify_wintesses:
                    import witnesscheck as wc

                    if wc.CHECKERS[algorithm](dea, witness):
                        print("witness passed", end="")
                    else:
                        print("witness failed", end="")
                print()
            else:
                print("File: %s ∈ %s" % (fil, algorithm))
        print("-" * 80)
