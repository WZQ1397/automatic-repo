# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-28 13:47
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

'''
读写文本格式的数据
read_csv
read_table
'''
data = DataFrame(np.arange(16).reshape(4, 4), index=list('abcd'), columns=['hhb', 'zjx', 'hcy', 'zjy'])
print(data)

data.to_csv('data/ex1.csv')

rdata = pd.read_csv('data/ex1.csv')
print(rdata)
#   Unnamed: 0  hhb  zjx  hcy  zjy
# 0          a    0    1    2    3
# 1          b    4    5    6    7
# 2          c    8    9   10   11
# 3          d   12   13   14   15

rdata = pd.read_table('data/ex1.csv', sep=',')
print(rdata)
#   Unnamed: 0  hhb  zjx  hcy  zjy
# 0          a    0    1    2    3
# 1          b    4    5    6    7
# 2          c    8    9   10   11
# 3          d   12   13   14   15

'''
配置默认名字
'''
# data=DataFrame(np.random.randn(3,4))
# print(data)
# #           0         1         2         3
# # 0  1.095597  0.454671  0.503149 -0.337012
# # 1 -0.688659 -1.455076  0.826556  0.823949
# # 2  1.122201  0.303618 -0.399119  0.979075
#
# data.to_csv('data/ex2.csv')

rdata = pd.read_csv('data/ex2.csv', header=None)
print(rdata)
#           0         1         2         3
# 0 -0.310421 -0.323209  0.996199  0.927549
# 1 -0.076534 -0.160730 -1.780651 -1.069414
# 2 -0.703372 -1.265776 -0.117108 -0.164619


# 配置名字
rdata = pd.read_csv('data/ex2.csv', names=['a', 'b', 'c', 'd'])
print(rdata)
#           a         b         c    d
# 0 -0.310421 -0.323209  0.996199  aaa
# 1 -0.076534 -0.160730 -1.780651  bbb
# 2 -0.703372 -1.265776 -0.117108  ccc

# 让d列成为行索引
names = ['a', 'b', 'c', '行索引']
rdata = pd.read_csv('data/ex2.csv', names=names, index_col='行索引')
print(rdata)
#          a         b         c
# 行索引
# aaa -0.310421 -0.323209  0.996199
# bbb -0.076534 -0.160730 -1.780651
# ccc -0.703372 -1.265776 -0.117108


'''
解读程序化
'''
# data=DataFrame(np.arange(16).reshape(8,2),index=[['one','one','one','one','two','two','two','one'],['a','b','c','d','a','b','c','d']],columns=['key1','key2'])
#
# data.to_csv('data/ex3.csv')


# value1,value2,key1,key2
# one,a,0,1
# one,b,2,3
# one,c,4,5
# one,d,6,7
# two,a,8,9
# two,b,10,11
# two,c,12,13
# one,d,14,15

rdata = pd.read_csv('data/ex3.csv', index_col=['value1', 'value2'])
print(rdata)
#           key1  key2
# value1 value2
# one    a          0     1
#        b          2     3
#        c          4     5
#        d          6     7
# two    a          8     9
#        b         10    11
#        c         12    13
# one    d         14    15

# 筛选阅读
rdata = pd.read_csv('data/ex4.csv', skiprows=[0, 2])
print(rdata)
#   value1 value2  key1  key2
# 0    one      a     0     1
# 1    one      b     2     3
# 2    one      c     4     5
# 3    one      d     6     7
# 4    two      a     8     9
# 5    two      b    10    11
# 6    two      c    12    13
# 7    one      d    14    15


data = pd.read_csv('data/ex5.csv')
print(data)
#   value1 value2  key1 key2
# 0    one    NaN     0    1
# 1    one      b     2    3
# 2    one      c     4   Na


# 指定NaN值
sentinels = {'key2': [3, 'Na'], 'value2': 'b'}
data = pd.read_csv('data/ex5.csv', na_values=sentinels)
print(data)
#   value1 value2  key1  key2
# 0    one    NaN     0   1.0
# 1    one    NaN     2   NaN
# 2    one      c     4   NaN

'''
逐块读取文件
'''
data = pd.read_csv('data/ex4.csv', nrows=2, skiprows=[0, 2])

print(data)
#   value1 value2  key1  key2
# 0    one      a     0     1
# 1    one      b     2     3


# 将数据分成块
chunker = pd.read_csv('data/ex3.csv', chunksize=2)
print(chunker)  # <pandas.io.parsers.TextFileReader object at 0x000000000B1B9F60>

tot = Series([])
for piece in chunker:
  tot = tot.add(piece['value1'].value_counts(), fill_value=0)

print(tot)
# one    5.0
# two    3.0
# dtype: float64
print(tot[0])

'''
输出文本格式，自定义分隔符
'''
data = pd.read_csv('data/ex3.csv')
print(data)

import sys

data.to_csv('data/ex6.csv', sep='|')
# |value1|value2|key1|key2
# 0|one|a|0|1
# 1|one|b|2|3
# 2|one|c|4|5
# 3|one|d|6|7
# 4|two|a|8|9
# 5|two|b|10|11
# 6|two|c|12|13
# 7|one|d|14|15

data = pd.read_csv('data/ex5.csv')
data.to_csv('data/ex7.csv', na_rep='null')  # 将空字符串定义为null
# ,value1,value2,key1,key2
# 0,one,null,0,1
# 1,one,b,2,3
# 2,one,c,4,Na

# 禁用索引
data.to_csv('data/ex8.csv', index=False, header=False)
# one,,0,1
# one,b,2,3
# one,c,4,Na

# 指定排列顺序
data.to_csv('data/ex9.csv', columns=['key1', 'key2', 'value1', 'value2'])
# ,key1,key2,value1,value2
# 0,0,1,one,
# 1,2,3,one,b
# 2,4,Na,one,c


'''
json
'''
import json

obj = '{"name":"hb","data":[1,2,3,4,5],"dict":[{"name":"aa"},{"name":"bb"}],"Na":1}'

# result=json.dumps(obj)
# print(result)

data = json.loads(obj)
print(data)

dict = DataFrame(data['dict'], columns=['name'])
print(dict)
#   name
# 0   aa
# 1   bb