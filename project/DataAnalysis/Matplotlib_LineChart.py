# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-01-15 18:21

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rc
# matplotlib inline
# TODO color ref: https://matplotlib.org/gallery/color/named_colors.html#sphx-glr-gallery-color-named-colors-py
# TODO line style ref: https://matplotlib.org/tutorials/introductory/pyplot.html#sphx-glr-tutorials-introductory-pyplot-py
time = np.arange(10)
temp = np.random.random(10)*30
Swdown = np.random.random(10)*100-10
Rn = np.random.random(10)*100-10

def figureSave(plt):
  plt.savefig('plt.png')
  plt.show()


def doubleYinline(time,temp,Swdown,Rn):
  rc('mathtext', default='regular')
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(time, Swdown, '--', label = 'Swdown')
  ax.plot(time, Rn, '--.', label = 'Rn')
  # twinx() / twiny()
  ax2 = ax.twinx()
  ax2.plot(time, temp, 'r-o', label = 'temp')
  # text(x_ray,y_ray,text_name,fontsize,)
  ax2.text(3, 1.5, 'Temperature', fontsize=12,)
  ax.legend(loc=2)
  ax.grid()
  ax.set_xlabel("Time (h)")
  ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  ax2.set_ylabel(r"Temperature ($^\circ$C)")
  ax2.set_ylim(0, 35)
  ax.set_ylim(-20,100)
  ax2.legend(loc=0)
  figureSave(plt)

# doubleYinline(time,temp,Swdown,Rn)

def combine_figure(time,temp,Swdown,Rn):
  fig = plt.figure()
  ax = fig.add_subplot(111)

  lns1 = ax.plot(time, Swdown, '-+', label='Swdown',color='plum')
  lns2 = ax.plot(time, Rn, 'k--', label='Rn')
  ax2 = ax.twinx()
  lns3 = ax2.plot(time, temp, 'g--^', label='temp')

  # added these three lines
  lns = lns1 + lns2 + lns3
  labs = [l.get_label() for l in lns]
  ax.legend(lns, labs, loc=0)

  ax.grid()
  ax.set_xlabel("Time (h)")
  ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  ax2.set_ylabel(r"Temperature ($^\circ$C)")
  ax2.set_ylim(0, 35)
  ax.set_ylim(-20, 100)
  figureSave(plt)

# combine_figure(time,temp,Swdown,Rn)

def curve_inline(time,temp,Swdown,Rn):
  # x = np.linspace(0,10)
  # y = np.linspace(0,10)
  # z = np.sin(x/3)**2*98

  x,y,z,o=time, temp, Swdown, Rn

  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(x,y, '-', label = 'Swdown')

  ax2 = ax.twinx()
  ax2.plot(x,z, 'b-d', label = 'Rn')
  ax2.plot(time, temp, 'g-p', label='temp')
  fig.legend(loc=1, bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)

  ax.set_xlabel("Time (h)")
  ax.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  ax2.set_ylabel(r"Temperature ($^\circ$C)")
  figureSave(plt)

# curve_inline(time,temp,Swdown,Rn)

def muti_figure(time,temp,Swdown,Rn):
  # 创建自变量数组
  # x = np.linspace(0, 2 * np.pi, 500)
  # 创建函数值数组
  # y1 = np.sin(x)
  # y2 = np.cos(x)
  # y3 = np.sin(x * x)
  x,y1,y2,y3 = time,temp,Swdown,Rn
  # 创建图形
  plt.figure(1)
  '''
  意思是在一个2行2列共4个子图的图中，定位第1个图来进行操作（画图）。
  最后面那个1表示第1个子图。那个数字的变化来定位不同的子图
  '''
  # 第一行第一列图形
  ax1 = plt.subplot(2, 2, 1)
  # 第一行第二列图形
  ax2 = plt.subplot(2, 2, 2)
  # 第二行
  ax3 = plt.subplot(2, 1, 2)
  # 选择ax1
  plt.sca(ax1)
  # 绘制红色曲线
  plt.plot(x, y1, color='red',lw=2.5,alpha=0.3)
  # 限制y坐标轴范围
  plt.ylim(0,35)
  ax1.set_xlabel("Time (h)")
  ax1.set_ylabel(r"Temperature ($^\circ$C)")
  # 选择ax2
  plt.sca(ax2)
  # 绘制蓝色曲线
  plt.plot(x, y2, 'b:')
  plt.ylim(-20, 100)
  ax2.set_xlabel("Time (h)")
  ax2.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")

  ax3.plot(x, y3, 'g-3', lw=0.5)
  # 选择ax3
  plt.sca(ax3)
  # bar chart
  ax3.bar(x, y3,alpha=0.5,align='center')
  plt.ylim(-20, 100)
  ax3.set_xlabel("Time (h)")
  ax3.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")

  plt.annotate('Predict', xy=(5,2), xytext=(3, 5.5),
               arrowprops=dict(facecolor='green', shrink=0.5),
               horizontalalignment='center', verticalalignment='top',
               )
  figureSave(plt)


muti_figure(time,temp,Swdown,Rn)

def embed_figure(time,temp,Swdown,Rn):
  # 定义figure
  fig = plt.figure()

  # 定义数据
  x = time

  # figure的百分比, 从figure 10%的位置开始绘制, 宽高是figure的80%
  left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
  # 获得绘制的句柄
  ax1 = fig.add_axes([left, bottom, width, height])
  # 绘制点(x,y)
  ax1.plot(x, temp, 'r')
  ax1.set_xlabel("Time (h)")
  ax1.set_ylabel(r"Temperature ($^\circ$C)")
  ax1.set_title('zach.wang')

  # 嵌套方法一
  # figure的百分比, 从figure 10%的位置开始绘制, 宽高是figure的80%
  left, bottom, width, height = 0.2, 0.6, 0.25, 0.25
  # 获得绘制的句柄
  ax2 = fig.add_axes([left, bottom, width, height])
  # 绘制点(x,y)
  ax2.plot(x, Swdown, 'b')
  ax2.set_xlabel("Time (h)")
  ax2.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  ax2.set_title('part1')

  # 嵌套方法二
  plt.axes([bottom, left, width, height])
  plt.plot(x, Rn, 'g')
  plt.xlabel("Time (h)")
  plt.ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  plt.title('part2')
  figureSave(plt)

# embed_figure(time,temp,Swdown,Rn)

def complex_figure_subplot2grid(time,temp,Swdown,Rn):
  plt.figure()
  # 通过栅格的形式创建布局方式,(3,3)创建3x3的布局形式，(0,0)绘制的位置，0行0列的位置绘制
  # colspan:表示跨几列 rowspan:表示跨几行
  layout = (3, 3)
  ax1 = plt.subplot2grid(layout, (0, 0), colspan=3)
  # 在ax1图中绘制一条坐标(1,1)到坐标(2,2)的线段
  ax1.plot(time, temp, 'r-p')
  ax1.set_xlabel("Time (h)")
  ax1.set_ylabel(r"Temperature ($^\circ$C)")
  # 设置ax1的标题  现在xlim、ylim、xlabel、ylabel等所有属性现在只能通过set_属性名的方法设置
  ax1.set_title('zach.wang')  # 设置小图的标题

  ax2 = plt.subplot2grid(layout, (1, 0), colspan=2, rowspan=2)
  ax2.plot(time,Swdown,'|-')
  ax2.plot(time,Rn,'.-')
  ax2.set_xlabel("Time (h)")
  ax2.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")
  ax3 = plt.subplot2grid(layout, (1, 2), rowspan=2)
  # ax4 = plt.subplot2grid(layout, (2, 0))
  # ax5 = plt.subplot2grid(layout, (2, 1))
  # 给对应的图绘制内容，这里只给ax4图绘制，属性通过set_xxx的模式设置
  ax3.scatter([1, 2], [2, 2])
  ax3.set_xlabel('ax3_x')
  ax3.set_ylabel('ax3_y')
  figureSave(plt)

# complex_figure_subplot2grid(time,temp,Swdown,Rn)

def complex_figure_gridspec(time,temp,Swdown,Rn):
  plt.figure()
  # 将整个视图分成3x3布局
  gs = gridspec.GridSpec(3, 3)
  print(gs)
  # gs[0,:]  指定画图的位置 前面指定该图所占的行范围0表示0行，1: 表示从第一行到最后一行
  # 第二个参数指定列的范围一个数表示固定列数，x:y表示从x列到y列
  ax1 = plt.subplot(gs[0, :])
  ax1.plot(time, temp, 'r-p')
  ax1.set_xlabel("Time (h)")
  ax1.set_ylabel(r"Temperature ($^\circ$C)")
  # 第一行，从0列开始到2列，不包括2，也就是占0、1两列
  ax2 = plt.subplot(gs[1, :2])
  ax2.plot(time,Swdown,'|-')
  ax2.plot(time,Rn,'.-')
  ax2.set_xlabel("Time (h)")
  ax2.set_ylabel(r"Radiation ($MJ\,m^{-2}\,d^{-1}$)")

  x = np.linspace(0, 2 * np.pi, 500)
  y1 = np.sin(x)
  y2 = np.cos(x)
  y3 = np.sin(x * x)
  # 从第一行到最后，占1、2两行，后面的2表示只占用第二列，也就是最后的一列
  ax3 = plt.subplot(gs[1:, 2])
  ax3.plot(x,y1)
  ax3.set_title("sin(x)")
  # 倒数第一行，只占第0列这一列
  ax4 = plt.subplot(gs[-1, 0])
  ax4.plot(x,y2)
  ax4.set_title("cos(x)")
  # 倒数第一行，只占倒数第二列，由于总共三列，所以倒数第二列就是序号1的列
  ax5 = plt.subplot(gs[-1, -2])
  ax5.plot(x,y3,'plum')
  ax5.set_title("sin(x^2)")
  figureSave(plt)

# complex_figure_gridspec(time,temp,Swdown,Rn)