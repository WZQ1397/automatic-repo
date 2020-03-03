# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-28 14:33
from __future__ import print_function
import pandas as pd
import numpy as np

# concatenating
# ignore index
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*2, columns=['a','b','c','d'])
# 上下拼接
res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

# join, ('inner', 'outer')
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'], index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['b','c','d','e'], index=[2,3,4])
# 左右拼接
res = pd.concat([df1, df2], axis=1, join='outer')
res = pd.concat([df1, df2], axis=1, join='inner')

# append
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['b','c','d', 'e'], index=[2,3,4])
# 追加内容
res = df1.append(df2,sort=True)
res = df1.append([df2, df3],sort=True)

s1 = pd.Series([1,2,3,4], index=['a','b','c','d'])
res = df1.append(s1, ignore_index=True)

print(res)
