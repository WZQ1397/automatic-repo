import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
##################################################
#  解决中文字体显示问题
font = {
    'family' : 'SimHei'
};
mpl.rc('font', **font);
##################################################
# 随机设置坐标值
# %matplotlib inline
N = 3
x = np.random.rand(N)
y = np.random.rand(N)
##################################################
fig = plt.figure(figsize=[8,4])
ax = fig.add_subplot(121)
# 绘制circle
for xi,yi in zip(x,y):
    circle = mpatches.Circle((xi,yi), 0.05, ec="blue",fc='blue')
    ax.add_patch(circle)
# 绘制Line 
line = mlines.Line2D(x,y,lw=3.,ls='-',alpha=1,color='red')
# set_zorder即设置对象的顺序 
line.set_zorder(1)
ax.add_line(line)
ax.set_title('先圆后线')

############################################
ax = fig.add_subplot(122)
# 绘制Line 
line = mlines.Line2D(x,y,lw=3.,ls='-',alpha=1,color='red')
ax.add_line(line)

# 绘制circle
for xi,yi in zip(x,y):
    circle = mpatches.Circle((xi,yi), 0.05, ec="blue",fc='blue')
    ax.add_patch(circle)
# set_zorder即设置对象的顺序 
line.set_zorder(0)
ax.set_title('先线后圆')
plt.show()
