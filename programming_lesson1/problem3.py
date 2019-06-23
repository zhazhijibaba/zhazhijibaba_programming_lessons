# coding=utf-8
# 窃取前人成果，站在巨人的肩膀上
# 应用现成的画图工具turtle
from turtle import *

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

exitonclick()
