# coding=utf-8
# 窃取前人成果，站在巨人的肩膀上
# 应用现成的画图工具turtle
from turtle import *

# Recursive function to draw a tree
# 画一棵树的工具（函数），先画树干，再画树枝
def drawTree(level):
    # stop at the end
    # 如果所有树枝都画完了，就停止
    if level == 0:
        return
    # 先画树干
    forward(level * 15)
    # draw left branch
    # 再画左边的下一层树枝
    left(20)
    drawTree(level - 1)
    # Draw right branch
    # 再画右边的下一层的树枝
    right(40)
    drawTree(level - 1)
    # go back to trunk
    # 退回到主树干
    left(20)
    backward(level * 15)

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
# 树干的层数
level = 5
# 应用画树干的函数, 画一个5层的树
drawTree(level)

exitonclick()
