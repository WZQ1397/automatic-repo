#PythonDraw.py
import turtle
num=800
turtle.setup(num,num,num,num)
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(15)
turtle.color("green")
for i in range(1,7):
    turtle.circle(80, -240)
    turtle.seth(-60*i)
turtle.done()