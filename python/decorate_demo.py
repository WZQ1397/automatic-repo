# author zach.wang
# -*- coding:utf-8 -*-
"""def help(ch):
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
help("x")


def basicuse2(fun):
    print("bbb")
    return fun

def basicuse():
    print("aaa")

basicuse = basicuse2(basicuse)
basicuse()

"""
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
        print("bbb")
    return basicuse2

@help3
def basicuse():
    print("aaa")

basicuse()
