#!/usr/bin/python

from pylab import *
#from  matplotlib import *
from matplotlib.font_manager import FontProperties

import pickle

data = pickle.load(file("stat.data"))

first  = lambda x: x[0]
second = lambda x: x[1]
third  = lambda x: x[2]

FORMAT = {
    'l12': 'r+',
    'b12': 'go',
    'l1': 'b*',  
    'b1': 'cs',
    'l32': 'yd',
    'b32': 'm^'
}

LABEL = {
    'l12': '$L_{1/2}$',
    'b12': '$B_{1/2}$',
    'l1': '$L_1$',  
    'b1': '$B_1$',
    'l32': '$L_{3/2}$',
    'b32': '$B_{3/2}$'
}

figure("Runtime Measurement")
yscale('log')

xlim([0 , 20])

for k,samples in data.items():
    samples = samples.items()

    x = map(first,samples)
    y = map(first, map(second, samples))
    e = map(second, map(second,samples))

    errorbar(x,y, yerr = e, fmt=FORMAT[k], label=LABEL[k])

legend()

savefig('foo.pdf')
show()
