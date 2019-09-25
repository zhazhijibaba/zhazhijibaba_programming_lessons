# compute pi using Nilakantha series
# pi = 3 + 4 / (2*3*4) - 4 / (4*5*6) + 4 / (6*7*8) = 4 / (8*9*10) + ...
# use the module decimal for high precision float number
from decimal import *

# set the precision how many digit
N = 20
getcontext().prec = N + 1
f = -1.0
pi = Decimal(str(3))
for x in range(2, N * 10000, 2):
    f = -1.0 * f
    pi += Decimal(str(4.0))/Decimal(str(f * x * (x + 1) * (x + 2)))
print "PI value = {1}".format(N, pi)
