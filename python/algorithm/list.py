# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2019-12-24 10:27
# import copy
#
lst = [1,20,[999]]
# newlst = lst
# deepcopylst_A = lst.copy()
# deepcopylst_B = copy.deepcopy(lst)
# lst[-1].append(888)
# print(newlst,deepcopylst_A,deepcopylst_B)
#
# print(dir(copy))
#
#
# letters = "THIS IS ZACHWANG"
# for letter in enumerate(letters):
#     print("The letter at index %i is %s" % letter)

# lst += [10]
# lst.pop()
# lst.extend([11,12])
# print(lst)


import copy
iterator = (i for i in range(1, 5))
matrix = [[(x,y) for y in iterator] for x in iterator]
matrix_minus = [[x*y for y in iterator] for x in iterator]
print(matrix,matrix_minus)

# expr=function
def inc(x):
   return x+1
print([inc(x) for x in range(10)])

# expr=expression
print([(x+1)**2 for x in range(10)])

# if判断 [expr for item in iterator if cond] / [expr for item in iterator if cond1 if cond2]
print([x for x in range(10) if x%2==0])

print([x for x in range(10) if x%2==0 if x>4])

print([(x,y) for x in range(10) if x%2==0 for y in range(10) if y>=8])


# for x in iterator:
print([(x,y) for x in range(1,3) for y in range(0,2)])


# 列表解析用于对可迭代对象做过滤和转换
print([(x+1,x+2) for x in range(5)])

print([{x:x+1} for x in range(5)])

print({x for x in range(10) if x%2!=0})

print({str(x):x for x in range(5)})


def f(x):
    return x*x

print(list(map(f,[1,2,3,4,5])))


# func可以是任意复杂的函数
print(list(map(str,[1,2,3,4,5])))

from functools import reduce
#把一个序列[1,3,5,7,9]变成int(13579)
def fn(x,y):
    return x*10+y

print(reduce(fn,[1,3,5,7,9]))


# 把str'13579'——>int(13579)
def str2int(s):
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]

    def fn(x,y):
        return x*10+y

    return reduce(fn,map(char2num,s))

print(str2int('13579'))

# 类似于sum(),实现一个阶乘prod()函数
def prod(lst):
    return reduce(lambda x,y:x*y,lst)

print(prod([1,2,3,4,5]))


import re
ss = """I figured it out.
I figured it? out from black and white Seconds and hours Maybe they had to take some time"""
ss_convert = re.sub('\n',' ',re.sub('[?!:.@()-]','',ss))
print(ss_convert)
words = ss_convert.split(' ')
d = {}.fromkeys(words,0)
for w in words:
    d[w] += 1
print(d)

# lambda
print(lambda : x for x in range(10))
print(y for y in (lambda : x for x in range(10)))

for x in range(10):
    y=lambda: x**x
    print(y)

powcal=lambda x,y=2: x**y
print(powcal(2,3))

lambdalist=[3,5,-4,-1,0,-2,-6]
ll=sorted(lambdalist,key=lambda x: abs(x),reverse=True)
print(lambdalist,ll)

# 应用在闭包中
def acculactor(x,adder=1):
    acc = lambda base=x, adder=adder: x + adder
    return acc()
# print(acculactor(5,5))

print(list(map(acculactor,[x for x in [y*y for y in range(5)]])))

from functools import reduce
print(reduce(acculactor,[x for x in [y*y for y in range(5)]]))

def tu(x,step=2,y=[]):
    # z = lambda x,step=step,y=y: map(y.append,zip(x,step))
    # print(list(z([3,5,-4,-1,0,-2,-6])))
    # for xi in x:
    #     y.append((xi,step))
    list(map(lambda xi: y.append((xi, step)), x))
    return y

print(tu([3,5,-4,-1,0,-2,-6]))

# y=[]
# print(map(lambda xi: y.append((xi,2)), [3,5,-4,-1,0,-2,-6]))
# print(y)

print(list(map(lambda x,f=lambda x,f:(f(x-1,f)+f(x-2,f)) if x>1 else 1: f(x,f),range(10))))

print(-22 // 10)