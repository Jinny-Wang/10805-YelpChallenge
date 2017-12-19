import sys
import numpy as np
from numpy import genfromtxt
import string
count = 0
total = 0

score = genfromtxt('metric_dist.csv')[1:]

print('mean',np.mean(score))
print('median',np.median(score))
