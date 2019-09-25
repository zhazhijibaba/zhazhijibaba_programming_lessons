# Compute pi value by Monte Carlo sampling
# circle area within a square with unit length
# pi = Area / r^2 
# Area = Area of the square * number of points within circle / total number of points
# Area of the square = 4 * r^2
# pi = 4.0 * number of points within circle / total number of points
import random
import math
import turtle

# initial turtle
tt = turtle.Turtle()
tt.hideturtle()
tt.color("black")
tt.speed(0)
tt.penup()
size = 100

# draw circle
tt.goto(0, -1.0 * size)
tt.pendown()
tt.circle(1.0 * size)
tt.penup()

# draw square
tt.goto(-1.0 * size, -1.0 * size)
tt.pendown()
for i in range(4):
    tt.forward(2.0 * size)
    tt.left(90)
tt.penup()

# setup Monte Carlo Sampling
# number of points for sampling
N = 100000
A = 0
r = 1.0
r2 = 1.0 * 1.0
for i in range(1, N + 1):
    # get random point
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    # check if the point is inside the circle
    c = False
    if x * x + y * y < r2:
        A += 1
        c = True
    ## show result every 100 steps
    if i % 100 == 0:
        if c:
            # show inside points in red
            tt.goto(x * size, y * size)
            tt.color("red")
            tt.dot()
        else:
            # show outside points in blue
            tt.goto(x * size, y * size)
            tt.color("blue")
            tt.dot()
        pi = 4.0 * A / i
        print "pi = {0} with {1} samples".format(pi, i)
        #print "{0} samples, calculated pi value = {1} with error {2} compared to math.pi {3}".format(i, pi, abs(pi - math.pi), math.pi)
