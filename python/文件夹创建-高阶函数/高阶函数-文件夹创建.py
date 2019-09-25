# author zach.wang0
# -*- coding:utf-8 -*-
import sys,getopt
from DirCreateMethod import *
arglst=""

def bysuffix(name=""):
    '''
    CREATE FILE NAME LIKE :  Xxx-1,Xxx-3 if you input the suffix name
    :param name: default -> none
    :return:
    '''
    return fun.suffix(name)

def byprefix(name=""):
    '''
    CREATE FILE NAME LIKE :  1-xxx,3-xxx if you input the prefix name
    :param name: default -> Zach
    :return:
    '''
    return fun.prefix(name)

def bydate(spec="today",count=0):
    '''
    CREATE FILE NAME LIKE :  1-xxx,3-xxx if you input the prefix name
    :param spec: default -> today FORMAT : 2019-09-04
    :return:
    '''
    if spec!="today" and not count:
        return fun.usedatetime(spec)
    else:
        return fun.usedatetime()

def full(spec,args):
    '''
    CREATE FILE NAME LIKE :  1-xxx,3-xxx if you input the prefix name
    :param spec: default -> today FORMAT : 2019-09-04
    :return:
    '''
    # print(args)
    byprefix(args[0])
    if len(args)>=2:
        bysuffix(args[1])
    else:
        bysuffix()
    # print("1", spec)
    return bydate(spec,len(args))

def deploy(func):
    '''
    A main 高阶函数调用入口函数
    :param func:
    :return:
    '''
    print("loading ...")
    # judge the num of args to execute
    Exec = func(funcarg,arglst) if len(arglst)>=1 else func(funcarg) if func.__name__!="full" else "ARGS ERROR!"
    return Exec

try:
   opts, args = getopt.getopt(sys.argv[1:],"hn:p:s:d:a",["prefix=","suffix=","date="])
except getopt.GetoptError:
    # raise getopt.GetoptError(str(opts) + 'which is not exists!')
    sys.exit(2)
for opt, arg in opts:
   if opt == '-n':
      num=arg
   elif opt in ("-p", "--prefix"):
      func ,funcarg = byprefix, arg
      if not bool(IsVaildName(funcarg)):
          raise AssertionError("Define "+ func.__name__ + " Name is invaild!")
   elif opt in ("-s", "--suffix"):
      func ,funcarg = bysuffix, arg
      if not bool(IsVaildName(funcarg)):
          raise AssertionError("Define " + func.__name__ + " Name is invaild!")
   elif opt in ("-d", "--date"):
      func ,funcarg = bydate, arg
      if not bool(IsVaildDate(funcarg)):
          raise AssertionError("Define Date format is invaild! must like XXXX-XX-XX")
      # print(arg)
   elif opt in ("-a", "--all"):
      func ,funcarg = full, arg
      # print(arg)
      arglst=sys.argv[5:]
   else:
       print(opt,arg)

fun = BatchDirDeploy(int(num))

# 使用eval()实现字符串转函数对象
# print(deploy(eval(sys.argv[2])))
deploy=CreateDir(deploy(func))
deploy.Create()


