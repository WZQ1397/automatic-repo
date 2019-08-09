from turtle import *
num=800
setup(num,num,num,num)
penup()
goto(0,-200)
pendown()
size=0.2
def curvemove():
    for i in range(int(100*size)):
        right(2/size)
        fd(2)
color('red','pink')
begin_fill()
left(140)
forward(111.65*size)
curvemove()
left(120)
curvemove()
forward(111.65*size)
end_fill()
done()