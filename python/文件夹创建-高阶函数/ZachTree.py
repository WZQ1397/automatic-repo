from functools import reduce
from Calculate import *
class Tree:

    def __init__(self,level,Type):
        self.Type=Type
        self.__level=level
        self.__singlelevel=0

    def nodes(self):
        # 高阶函数
        return reduce(binarycounts if self.Type== "binary" else simplecounts ,range(1,self.__level+1))

    def levelsummary(self,scope,sum):
        levelnum, level, index =[],{},1
        for i in scope:
            levelnum.append("Level-"+str(index))
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
        return self.nodes(),self.levelsummary(scope,sum)