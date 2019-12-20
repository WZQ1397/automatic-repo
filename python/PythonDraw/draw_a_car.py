# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-20 16:59
import turtle

WINDOWS_HEIGHT=500
WINDOWS_WIDTH=500
turtle.setup (width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT, startx=0, starty=0)
# 直接显示
turtle.tracer(0)

def draw_wheel(radius=100,pos=(0,0),filled=False,color='black'):
  circle = turtle.Turtle()
  circle.hideturtle()
  circle.penup()
  circle.goto(pos)
  circle.pendown()
  circle.color(color)
  if filled:
    circle.begin_fill()
    circle.circle(radius)
    circle.end_fill()
  else:
    circle.circle(radius)
  circle.penup()
  circle.right(90)
  circle.forward(-75)
  circle.pendown()
  circle.right(90)
  circle.color('red')
  circle.circle(30)
  circle.pensize(5)
  circle.right(90)
  circle.penup()
  circle.forward(-28)
  circle.pendown()
  circle.dot(20,'gray')

def draw_windows(color='gray'):
  window = turtle.Turtle()
  window.penup()
  window.color(color)
  window.goto(-20,190)
  window.pendown()
  window.begin_fill()
  window.right(90)
  window.forward(50)
  window.left(90)
  window.forward(100)
  window.end_fill()
  window.penup()
  window.forward(-120)
  window.pendown()
  window.begin_fill()
  for _ in range(4):
    window.left(90)
    window.forward(50)
  window.end_fill()
  window.penup()
  window.forward(-70)
  window.pendown()
  window.begin_fill()
  window.left(90)
  window.forward(50)
  window.left(90)
  window.forward(50)
  window.left(55)
  window.forward(60)
  window.end_fill()


def draw_car(Type='taxi'):
  car = turtle.Turtle()
  # car.hideturtle()
  turtle.title(type)
  car.pu()
  car.goto(-WINDOWS_WIDTH//2 + 50, WINDOWS_HEIGHT/2.5)
  car.color('green')
  car.shape('arrow')
  car.begin_fill()
  # top
  car.forward(50)
  car.pd()
  car.forward(150)
  # front glass
  car.right(30)
  car.forward(100)
  # engine gap
  car.left(30)
  car.forward(50)
  # car head
  for x in range(60):
    car.right(1.5)
    car.forward(2)
  car.forward(20)
  # car buttom
  car.right(90)
  car.forward(430)
  #car backend
  car.right(90)
  car.forward(80)
  # car backend glass
  car.right(40)
  car.forward(90)
  car.penup()
  car.end_fill()
  draw_wheel(45,(-120,-10),True)
  car.forward(200)
  draw_wheel(45,(120,-10),True)
  draw_windows()





if __name__ == '__main__':
    # draw_star(15,'xlarge')
    draw_car()
    # 防止退出
    turtle.mainloop()
