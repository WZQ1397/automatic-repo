#PythonDraw.py
import turtle
turtle.setup(800, 800, 800, 800)
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(25)
turtle.color("green")
turtle.seth(-40)
for i in range(4):
    turtle.circle(40, 80)
    turtle.circle(-40, 80)
turtle.circle(40, 80/2)
turtle.fd(40)
turtle.circle(16, 360)
turtle.fd(40 * 2/3)
turtle.done()