from turtle import *
num=800
setup(num,num,num,num/2)

def drawStick():
    pensize(15)
    color('black')
    pd()
    left(90)
    fd(550)

def drawFlag():
    pensize(2)
    begin_fill()
    color('red', 'pink')
    right(90)
    fd(400)
    right(90)
    fd(200)
    right(90)
    fd(400)
    end_fill()

def drawStar():
    color('yellow')
    penup()
    goto(-170, 140)
    pd()
    write("★", font=("Times", 48, "bold"))
    for x, y in ((-110, 210), (-90, 180), (-90, 150), (-110, 120)):
        pu()
        goto(x, y)
        write("★", font=("Times", 18, "bold"))

def drawChinaFlag():
    penup()
    goto(-200, -300)
    drawStick()
    drawFlag()
    drawStar()
    pendown()
    hideturtle()
    done()

drawChinaFlag()
