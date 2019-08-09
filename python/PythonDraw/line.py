import turtle,math
num=800
turtle.setup(num,num,num,num)
N=7

def mutiangle(size):
    turtle.penup()
    i=1
    print(size,-size*300)
    tag=size/math.sqrt(N)
    turtle.goto(-150*tag,-size*100-N*10)
    turtle.pendown()

    turtle.fd(300*tag)
    while i < N:
        turtle.left(360/N)
        turtle.fd(300*tag)
        i+=1
    return size

def shapenum(num):
    size=2.0
    for i in range(0,num):
        size-=size/num
        size=mutiangle(size)
        turtle.seth(0)


shapenum(10)

turtle.done()


