# coding=utf-8
# 窃取前人成果，站在巨人的肩膀上
# 应用现成的画图工具turtle
from turtle import *

# Recursive function to draw a tree
# 画一棵树的工具（函数），先画树干，再画树枝
def drawTree(level, length, ratio, theta1, theta2):
    # stop at the end
    # 如果所有树枝都画完了，就停止
    if level == 0:
        return
    # 先画树干
    forward(length * ratio)
    # draw left branch                                                 
    # 再画左边的下一层树枝
    left(theta1)                                                       
    drawTree(level - 1, length * ratio, ratio, theta1, theta2)         
    # Draw right branch                                                
    # 再画右边的下一层的树枝
    right(theta1 + theta2)                                             
    drawTree(level - 1, length * ratio, ratio, theta1, theta2)         
    # go back to trunk
    # 退回到主树干
    left(theta2)
    backward(length * ratio)                                   
                                                                       
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
# 每层树干的长度比例
ratio = 1.0
# 左侧树枝的角度
theta1 = 20
# 右侧树枝的角度
theta2 = 20
# 树干的长度
length = 150 / level
# 应用画树干的函数, 画一个5层的树
drawTree(level, length, ratio, theta1, theta2)

exitonclick()
