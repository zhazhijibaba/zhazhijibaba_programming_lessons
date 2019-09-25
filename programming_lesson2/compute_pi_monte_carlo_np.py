# Compute pi value by Monte Carlo sampling
# circle area within a square with unit length
# pi = Area / r^2 
# Area = Area of the square * number of points within circle / total number of points
# Area of the square = 4 * r^2
# pi = 4.0 * number of points within circle / total number of points
import random
import numpy as np
import math

# number of points for sampling
N = 100000
r = 1.0
r2 = 1.0 * 1.0
A = 0
ii = 10000
for i in range(ii):
    xy = np.random.rand(2, N)
    xy2 = np.square(xy)
    A += np.sum(np.add(xy2[0,:], xy2[1,:]) < r2)
    pi = 4.0 * A / N / (i + 1)
    print "{0} samples, calculated pi value = {1} with error {2} compared to math.pi {3}".format(N * (i + 1), pi, abs(pi - math.pi), math.pi)
#pi = 4.0 * A / N / ii 
#print "{0} samples, calculated pi value = {1} with error {2} compared to math.pi {3}".format(N * ii, pi, abs(pi - math.pi), math.pi)
