# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-20 13:32

import turtle
import time
from random import randrange

WINDOWS_HEIGHT=500
WINDOWS_WIDTH=500
turtle.setup (width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT, startx=0, starty=0)
# 直接显示
# turtle.tracer(0)
# 调节速度
turtle.speed(-1)
def draw_star(num=1,size="default"):
  SIZELIST = {'small': 50, 'default': 100, 'large': 200 , 'xlarge':300}
  star = turtle.Turtle()
  star.pensize(5)
  star.pencolor("yellow")
  star.fillcolor("red")
  star.pu()
  for _ in range(num):
    star.begin_fill()
    xray_right_margin =WINDOWS_WIDTH //2 -SIZELIST[size]
    yray_top_margin=WINDOWS_HEIGHT//2-SIZELIST[size]*0.3
    yray_buttom_margin=-WINDOWS_HEIGHT//2+SIZELIST[size]*0.6
    xray=randrange(-WINDOWS_WIDTH//2,xray_right_margin)
    yray=randrange(yray_buttom_margin,yray_top_margin)
    print((xray,yray))
    star.goto(xray,yray)
    star.pd()
    #
    # star.write((xray,yray), font=('Arial', 40, 'normal'))
    for _ in range(5):
      star.forward(SIZELIST[size])
      star.right(144)
    star.end_fill()
    star.pu()
    # star.hideturtle()
  time.sleep(2)

  star.penup()
  star.goto(-150, -120)
  star.color("violet")
  star.write("Done", font=('Arial', 40, 'normal'))


def draw_flower(size=200):
  flower= turtle.Turtle()
  flower.color("red", "yellow")
  flower.begin_fill()
  flower.goto(-size//2,0)
  for _ in range(50):
    flower.forward(size)
    flower.left(170)
  flower.end_fill()
  turtle.mainloop()


def draw_fan(size=200):
  fan= turtle.Turtle()
  fan.hideturtle()
  fan.color("gray", "brown")
  fan.goto(0,-size//2)
  fan.left(30)
  fan.pendown()
  fan.pensize(5)
  fan.begin_fill()
  for _ in range(40):
    fan.forward(size)
    fan.forward(-size)
    fan.left(3)
  fan.end_fill()
  turtle.mainloop()

if __name__ == '__main__':
    draw_fan()