x = [chr(_) for _ in range(ord('a'), ord('z')+1)]
print(x)
print("{0:-^50}".format("generator"))

y = (chr(_) for _ in range(ord('a'), ord('z')+1))
print(y.__next__(),"---")
print(next(y),"---")
for alpha in y:
    print(alpha,end="")



# --------------------generator---------------------
# a ---
# b ---
# cdefghijklmnopqrstuvwxyz

def fib():
    x, y = 0, 1
    while True:
        yield x
        x, y = y, x+y
        print(x,"---")
        yield y
        print(y,"+++")

inst = fib()
i=0
while(i<10):
    next(inst)
    i+=1


import string
res = filter(lambda n:n>5,range(10))
for x in res:
    print(x,end=" ")
res = filter(lambda n:not(n%3 and n%7),range(100))
for x in res:
    print(x,end=" ")
print(" ")
res = zip(map(lambda alpha:alpha,range(ord('a'), ord('z')+1)),string.ascii_lowercase)
for x in res:
    print(x,end=" ")
