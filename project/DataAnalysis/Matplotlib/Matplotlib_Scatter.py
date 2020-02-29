# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-03 21:35
# import <module_name> [as <alias_name>]
import matplotlib.pyplot as plt
import math
import matplotlib
xlist = []
ylist = []
startnum = -2
while startnum <= 2:
  xlist.append(startnum)
  ylist.append(math.sin(startnum))
  startnum = startnum +0.5
# scatter(x,y) used to draw a point
plt.scatter(xlist,ylist,alpha=0.5)
# show a figure
# plt.show()
matplotlib.pyplot.show()

