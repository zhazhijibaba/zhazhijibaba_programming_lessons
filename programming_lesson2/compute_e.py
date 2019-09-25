# Euler's number e, the base of natural logs
# e is the sum of this infinite series:
# e = 1/0! + 1/1! + 1/2! + 1/3! + 1/4! + ...
# use the module decimal for high precision float number

# set the precision
N = 100
fact = 1
euler = 1
for x in range(1, N):
    fact = fact * x
    euler += 1.0 / fact
print "Eulers number = {0}".format(euler)
