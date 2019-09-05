# author zach.wang
# -*- coding:utf-8 -*-

def highfunc(ch):
    '''
    This is a 高阶函数
    :param ch: type str
    :return:
    '''
    def basic(choice):
        if choice == "a":
            basicuse()
        else:
            basicuse2()
    def basicuse2():
        print("bbb")
    def basicuse():
        print("aaa")
    basic(ch)
highfunc("x")

help(highfunc)


def basicuse2(fun):
    print("bbb")
    return fun

def basicuse():
    print("aaa")

basicuse = basicuse2(basicuse)
basicuse()


def help2(fun):
    def basicuse2():
        fun()
        print("bbb\n----")
    return basicuse2

def basicuse():
    print("aaa")

basicuse = help2(basicuse)
basicuse()



def help3(fun):
    def basicuse2():
        fun()
        print("bbb\n++++")
    return basicuse2

@help3
def basicuse():
    print("aaa")

basicuse()

#--------------

def help5(fun):
    def basicuse2(*args,**kwargs):
        print("before\n")
        res = fun(*args,**kwargs)
        print("bbb\n",res)
    return basicuse2

@help5   #help5 = basicuse(help5)
def basicuse(x,y,z):
    print("aaa",x,y,z)
    return "ok"

basicuse("wzq","lts",[chr(_) for _ in range(ord('a'), ord('z')+1)])
