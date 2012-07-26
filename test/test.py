"""
run all tests
"""

import sys, os

if not os.getcwd().endswith("test"):
    os.chdir("test")

sys.path.insert(0, os.path.abspath('../src/'))


import trap
from basic_alg_test import *
from dea_test import *

import unittest
if __name__ == '__main__':
    unittest.main()
