import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

fig = plt.figure(figsize=[8,4])
ax = fig.add_subplot(121)
# 绘制circle
x=np.array([0.4,0.5,0.6,0.55,0.45])*2
y=np.array([0.4,0.5,0.4,0.3,0.3])*2

colors=['red','orange','yellow','green','blue']
for i,xi,yi in zip(np.arange(len(x)),x,y):
    circle = mpatches.Circle((xi,yi), 0.2, ec='pink',fc='pink')
    circle.set_zorder(i)
    ax.add_patch(circle)

circle = mpatches.Circle((1,0.8), 0.1, ec="white",fc="white")
ax.add_patch(circle)
circle.set_zorder(10)

x=np.array([0.4,0.5,0.6,0.55,0.45])*2+1
y=np.array([0.4,0.5,0.4,0.3,0.3])*2

xl=[1,1]
yl=[0,0.55]
line = mlines.Line2D(xl,yl,lw=3.,ls='-',alpha=1,color='green')
line.set_zorder(0)
ax.add_line(line)
colors=['red','orange','yellow','green','blue']
for i,xi,yi in zip(np.arange(len(x)),x,y):
    circle = mpatches.Circle((xi,yi), 0.2, ec=colors[i],fc=colors[i])
    circle.set_zorder(i)
    ax.add_patch(circle)

circle = mpatches.Circle((2,0.8), 0.1, ec="white",fc="white")
ax.add_patch(circle)
circle.set_zorder(10)

xl=[2,2]
yl=[0,0.55]
line = mlines.Line2D(xl,yl,lw=3.,ls='-',alpha=1,c='green')
line.set_zorder(0)
ax.add_line(line)
ax.set_xlim([0,2.5])
ax.set_ylim([0,2.5])
plt.show()

