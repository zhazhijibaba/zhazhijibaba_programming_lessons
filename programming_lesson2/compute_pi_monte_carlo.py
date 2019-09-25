# Compute pi value by Monte Carlo sampling
# circle area within a square with unit length
# pi = Area / r^2 
# Area = Area of the square * number of points within circle / total number of points
# Area of the square = 4 * r^2
# pi = 4.0 * number of points within circle / total number of points
import random
import math

# number of points for sampling
N = 100000
A = 0
r = 1.0
r2 = 1.0 * 1.0
for i in range(N):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    if x * x + y * y < r2:
        A += 1
pi = 4.0 * A / N
print "{0} samples, calculated pi value = {1} with error {2} compared to math.pi {3}".format(N, pi, abs(pi - math.pi), math.pi)
