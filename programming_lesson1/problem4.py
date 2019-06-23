# coding=utf-8
# 窃取前人成果，站在巨人的肩膀上
# 应用现成的画图工具turtle
from turtle import *

# Recursive function to draw a tree
# 画一棵树的工具（函数），先画树干，再画树枝
def drawTree():
    # 画主树干，长75
    forward(75)
    # draw left branch
    # 调整树枝角度20度
    left(20)
    # 然后先画左边的树枝,长60
    forward(60)
    # 退回主树干
    backward(60)
    # Draw right branch
    # 调整右侧树干的角度，向右40度
    right(40)
    # 然后再画右边的树枝,长60
    forward(60)
    # 退回主树干
    backward(60)
    # go back to trunk
    # 调整返回主树干的角度
    left(20)
    # 退回主树干底端
    backward(75)

# set up initial state
# 初始化的执行函数
# 让海龟爬到屏幕下方中间的位置
def initial():
    # 抬起画笔
    up()
    # 向左转90度
    left(90)
    # 向后退100个像素
    backward(100)
    # 按下画笔，开始画画
    down()

# set up initial state
# 初始化, 让海龟爬到屏幕下方中间的位置
initial()

# draw a tree using a recursive function
# 画树干的函数, 先画一个Y字形的树干
drawTree()

exitonclick()
