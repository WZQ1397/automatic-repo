from math import sqrt
from sys import argv
from ZachTree import Tree as Ztree
from Calculate import *
class ZHelp(Exception):
    def __init__(self,ERRType=""):
        self.ERRType=ERRType

    def Usage(self):
        '''
        python3 内置高阶函数-树的创建.py ARGS1
        :param ARGS1 ==> simple | binary
        :return: TREE FIGURE AND COUNTS
        '''

    def Error(self):
        print('\033[1;31;40m')
        print('*' * 50)
        print('\033[7;31m错误，',self.ERRType,'，系统退出！\033[1;31;40m')  # 字体颜色红色反白处理
        print('*' * 50)
        print('\033[0m')
        exit(255)

@TimeWatcher
def exec(level,Type):
    width=level*int(sqrt(level))

    try:
        # 这个是实例
        CreateTree=Ztree(level, Type)

        '''
        CreateTree.Type="zach"  创建实例属性
        Ztree.Type="zach"       创建类属性
        '''
        # TODO  CreateTree.chkvaild 静态方法调用
        if Type.lower() == "help" or not CreateTree.chkvaild(Type):
            help(ZHelp("use").Usage)
            exit(0)
        v=CreateTree.tree
        '''
        调用类，直接使用__str__方法返回值
        '''
        print(CreateTree)
        for level,num in v.items():
            print(level,": ",num)
        # TODO 手动删除对象 --> 调用类中的__del__方法清理垃圾
        del v
    # 多个异常需要使用元祖
    except (AttributeError,ValueError) as e:
       ZHelp(e).Error

if __name__ == "__main__":
    # 直接运行部分
    try:
        exec(int(argv[1]),str(argv[2]))
    except IndexError as e:
        ZHelp(e).Error()
        help(ZHelp.Usage)
    except NameError as e:
        ZHelp(e).Error()
        help(ZHelp.Usage)

else:
    # 使用模块调用部分
    assert argv[1].isdigit()
    if len(argv)>2:
        assert str(argv[2]).lower() == "binary" or str(argv[2]).lower() == "simple"
        exec(eval(argv[1]),eval(argv[2]))
    else:
        exec(eval(argv[1]))