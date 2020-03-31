# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-03-31 9:32

import jmespath
source = {"a": {
  "b": {
    "c": [
      {"d": [0, [1, 2, {'x':10,'y':20,'z':30}]]},
      {"d": [3, 4]}
    ]
  }
}}
# 下标操作，仅用于数组
result = jmespath.search('a.b.c[0]',source)
print(result)
# 下标操作，仅用于数组
result = jmespath.search('a.b.c[0].d[0]',source)
print(result)
# 下标和.操作符混合操作
result = jmespath.search('a.b.c[0].d[1][0]',source)
print(result)
# 切片
result = jmespath.search('a.b.c[0].d[-1][::2]',source)
print(result)
# List Projections列表投影
result = jmespath.search('a.b.c[0].d[*]',source)
print(result)
# Object Projections对象投影
result = jmespath.search('a.b.*',source)
print(result)
# Pipe 过滤
result = jmespath.search('a.b.* | [0][-1]',source)
print(result)
# Pipe 过滤 + MultiSelect
result = jmespath.search('a.b.* | [0][0] | d[-1][-1] | [x,y]',source)
print(result)
# Pipe 过滤 + MultiSelect + JSON KeyName
result = jmespath.search('a.b.* | [0][0] | d[-1][-1] | {First:x,Second:y}',source)
print(result)
# Pipe 过滤 + MultiSelect + 内置函数
# https://jmespath.org/specification.html#functions
result = jmespath.search('length(a.b.* | [0][0] | d[-1][-1])',source)
print(result)
# Pipe 过滤 + MultiSelect
result = jmespath.search('a.b.* | [0][0] | d[-1][-1] | *  ',source)
print(result)
# Pipe 过滤 + MultiSelect ???
result = jmespath.search('a.b.* | [0][0] | [?d[-1][-1] == `10`] | [0]  ',source)
print(result)