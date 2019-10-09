from functools import reduce
from math import sqrt
from Calculate import *
class Tree:
    '''
    限定Person对象只能绑定Type, __level, __singlelevel属性
    需要注意的是__slots__的限定只对当前类的对象生效，对子类并不起任何作用。
    '''
    __slots__ = ('Type', '__level', '__singlelevel')

    def __init__(self,level,Type):
        self.Type=Type
        self.__level=level
        self.__singlelevel=0

    @staticmethod
    def chkvaild(choice:str) -> bool:
        '''
        静态方法：作为工具方法和当前类没有关系，没有默认第一个参数
        实例方法第一个参数是self，类方法第一个参数是cls
        静态方法和类方法都是通过给类发消息来调用的
        '''
        return True if choice.lower() in ['binary','simple'] else False

    @property
    def nodes(self) -> int:
        # 高阶函数
        return reduce(binarycounts if self.Type== "binary" else simplecounts ,range(1,self.__level+1))

    def levelsummary(self,scope,sum):
        levelnum, level, index =[],{},1
        for i in scope:
            '''
            format: str.join(["xxx",xxx]) 
            EG: "|".join([1,2,3]) ==> 1|2|3
            '''
            levelnum.append("".join(["Level-",str(index)]))
            # print(levelnum)
            sum=Calc(i, self.Type)
            level[levelnum[i-1]]=sum.levelcounts
            index += 1
        return level

    def simple(self,level):
        return level

    def binary(self,level):
        return 2**(level-1)

    @property
    def tree(self):
        '''
        使用了属性装饰器后，直接使用函数名就可以返回值，否在需要执行函数
        使用前：tree(x,Type).tree()
        使用后：tree(x,Type).tree
        :return:
        '''
        scope=range(1,self.__level+1)
        sum=Calc(self.__level, self.Type)
        # if self.Type == "binary":
        #     muti=binary
        # else:
        #     muti=simple

        for i in scope:
            # 多态 eval()实现
            Tree= " + "*eval("self."+self.Type)(i)
            print(Tree.center(sum.levelcounts*3))

        return self.levelsummary(scope,sum)

    def __str__(self):
        '''
        尝试把Tree的值转换为字符串
        :return:
        '''
        width = self.__level * int(sqrt(self.__level))
        return "nodes: {}".format(self.nodes).center(width)

    def __del__(self):
        '''
        手动清理垃圾对象，Python 默认会自动清理
        :return:
        '''
        return "Class",self.__class__.__name__,"has been deleted"