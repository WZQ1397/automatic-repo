from functools import reduce
import  time

def simplecounts(start, end):
    #print(start,end)
    return (lambda start, end: start + end)(start, end)

def binarycounts(_,x):
    '''
    s=lambda x,calc:1 if x==1 else calc(x-1,calc)+2 ** (x - 1)
    (lambda x,s:s(x,s))(x)
    :param _: throw away
    :param x:
    :return:
    '''
    return (lambda x,s=lambda x,calc:1 if x==1 else calc(x-1,calc)+2 ** (x - 1):s(x,s))(x)


class Calc:
    def __init__(self,level,Type):
        self.__Type=Type
        self.__level=level

    @property
    def 阶乘(self):
        x = self.__level
        return (lambda x : 阶乘(x - 1) * x if x > 1 else 1)(x)

    @property
    def levelcounts(self):
        return 2**(self.__level-1) if self.__Type == "binary" else self.level

class TimeWatcher:
    '''
    类装饰器 ：内置方法 def __call__(self, *args, **kwargs):
    '''
    def __init__(self,func):
        self.__func=func

    def __call__(self,level,Type):
        start = time.clock()
        self.__func(level,Type)
        end = time.clock()
        print("time used:", end - start)


def CountTreeNodes(Type,final) -> object:
    '''
    高阶函数--闭包方式
    :param Type:
    :param Total:
    :param final:
    :return:
    '''

    def simplecounts(flag):
        print("inner:", flag)
        func=lambda flag: flag+func(flag-1) if flag >=1 else 1
        return func(flag)
        # if flag >=1 :
        #    return flag+simplecounts(flag-1)
        # else:
        #     return 1

    def binarycounts(flag):
        '''
        s=lambda flag,calc:1 if flag==1 else calc(flag-1,calc)+2 ** (flag - 1)
        (lambda flag,s:s(flag,s))(flag)
        :param Total:
        :param flag:
        :return:
        '''
        return (lambda flag,s=lambda flag,calc:1 if flag==1 else calc(flag-1,calc)+2 ** (flag - 1):s(flag,s))(flag)

    try:
        Type = simplecounts if Type=="simple" else binarycounts
    except UnboundLocalError as e:
        Type = simplecounts

    return Type(final)


#print(CountTreeNodes("simple",7))

