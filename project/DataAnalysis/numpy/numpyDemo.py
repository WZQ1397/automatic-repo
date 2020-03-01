# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-24 15:27


import numpy as np
# 矩阵是可变类型
# 固定创建2*4数组类型为int64
array = np.array([[1,2,3,4],
                 [2,3,4,5]],dtype=np.int64)
array_A = array
# 把数组转换成一维数组
xray = array_A.reshape(array_A.size)
yray = array_B = np.arange(8)
def getArrayInfo(array):
  print("values:\n",array)
  print("dimension:",array.ndim)
  print("shape:",array.shape)
  print("size:",array.size)
  print("datatype:",array.dtype)

def initRandArray():
  # 生成3*2全0二维浮点类型数组
  zeroarray = np.zeros(shape=(3,2),dtype=np.float16)
  print(zeroarray)
  # 生成3*3*2全0三维布尔类型数组
  emptyarray = np.empty(shape=(3,3,2),dtype=np.bool)
  print(emptyarray)
  # 生成3*4,数值为[1,25), 步长为2, 的二维布尔类型数组
  nprange = np.arange(1,25,2).reshape((3,4))
  print(nprange)
  # 生成5*4,数值为[1,25), 线性增长的二维布尔类型数组, 共20个数据项
  nplinerange = np.linspace(1,25,20).reshape((5,4))
  print(nplinerange)

def calcArray(array_A,array_B):
  array_A_single = array_A.reshape(array_A.size)
  # 同一index上数值相减
  print(array_A_single-array_B)
  # 同一index上数值相乘
  print(array_A_single*array_B)
  # 同一index上数值的幂 EG: array_A_single[1]**array_B[1]
  print(array_A_single**array_B)
  print(array_A_single*np.sin(1))
  # 判断每个值是否大于3
  print(array_A_single>3)
  array_B = array_B.reshape(4,2)
  # 矩阵运算
  print(np.dot(array_A,array_B))
  print(array_A.dot(array_B))

def generateArrayAndAggerateCalc(xray,yray):
  nprand = np.random.random((2,4))
  # print(nprand)
  # 生成9个 范围[-100,100] 的值，数据类型是int
  nprandint = np.random.randint(-100,100,9,'i')
  # print(nprandint)
  # # 聚合运算
  # print(nprandint.sum(),nprandint.min(),nprandint.mean())
  # 设置上限
  yray = (yray+1) * 5
  # 下线为xray, 上限为yray
  nprandint2D_A = np.random.randint(xray, yray,dtype=np.uint16)
  # print(nprandint2D_A)
  # print(nprandint2D_A.sum(),nprandint2D_A.min(),nprandint2D_A.mean())

  xray_2D = xray.reshape(4,2)
  yray_2D = yray.reshape(4,2)
  # 生成一个二维限值数组
  nprandint2D_B = np.random.randint(xray_2D, yray_2D,dtype=np.uint16)
  print(nprandint2D_B)
  # # 对数组的(2,1)位置取值
  # print(nprandint2D_B[2][1],nprandint2D_B[2,1],nprandint2D_B[2,1:])
  # # 获取数组的第三行
  # print(nprandint2D_B[2],nprandint2D_B[2,],nprandint2D_B[2,:],nprandint2D_B[2:])
  print("sum:",nprandint2D_B.sum(axis=0),"\nget min in vertical:",
        nprandint2D_B.min(axis=1),"\nget avg in horizon:",
        nprandint2D_B.mean(axis=0),"\n middle num:",
        np.median(nprandint2D_B),"\ncummlatesum in horizon:",
        nprandint2D_B.cumsum(axis=1),"\ndifference:",
        np.diff(nprandint2D_B),"\njudge non-zero position:",
        nprandint2D_B.nonzero(),"\nAfter sort:",
        np.sort(nprandint2D_B))

  print("\nmax in all values:",nprandint2D_B.argmax(),
        "\nmin in all values:",nprandint2D_B.argmin(),
        "\nsort pos in vertical:",nprandint2D_B.argsort(axis=0))
  # 数组转置方法
  print("\narray transform:\n",nprandint2D_B.T)
  print(np.transpose(nprandint2D_B,axes=(1,0)))
  print(np.transpose(nprandint2D_B,axes=(0,1)))
  # 拟合数值,低于最小值,就设置最小值; 高于最大值, 就设置最大值
  print(np.clip(nprandint2D_B,0,9))
  # 把二维数组转成一维
  print(nprandint2D_B.flatten(),nprandint2D_B.flat)
  # 迭代对象
  for v in nprandint2D_B.flat:
    print(v,end="|")



def arrayMerge(xray,yray,output=0):
  # 数组转置两种方法
  get_shape=xray.shape
  try:
    xrayT = xray.reshape(-1,get_shape[2])
  except IndexError as e:
    xrayT = xray.reshape(-1,1)

  yrayT = yray[:,np.newaxis]
  if output:
    # 数组上下合并
    print(np.vstack((xray,yray)))
    # 数组左右合并
    print(np.hstack((xray,yray)))
    print(xrayT)
    print(yrayT)
    # 多组数据合并, axis=0上下合并, axis=1左右合并
    print(np.concatenate((xrayT,yrayT,xrayT),axis=1))
  return np.concatenate((xrayT,yrayT,xrayT),axis=1)

def arraySplit(xray,yray):
  bigArray = arrayMerge(xray,yray)
  print(bigArray)
  # 等量分割
  # axis=0上下分割, axis=1左右分割 [注意: 分割后数量必须相等, 否则报错]
  print(np.split(bigArray,2,axis=0))
  print(np.split(bigArray,3,axis=1))
  print(np.vsplit(bigArray,2))
  print(np.hsplit(bigArray,3))
  # 不等分割
  print(np.array_split(bigArray,3,axis=0))


# arraySplit(xray,yray)

# arrayMerge(xray,yray)
# initRandArray()
# getArrayInfo(array)
# calcArray(array_A,array_B)
generateArrayAndAggerateCalc(xray,yray)
