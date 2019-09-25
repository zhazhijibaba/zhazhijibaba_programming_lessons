# Euler's number e, the base of natural logs
# e is the sum of this infinite series:
# e = 1/0! + 1/1! + 1/2! + 1/3! + 1/4! + ...
# use the module decimal for high precision float number
from decimal import *

# set the precision
N = 50
getcontext().prec = N + 1
fact = 1
euler = 1
for x in range(1, N):
    fact = fact * x
    euler += Decimal(str(1.0))/Decimal(str(fact))
print "Eulers number with {0} digit = {1}".format(N, euler)
