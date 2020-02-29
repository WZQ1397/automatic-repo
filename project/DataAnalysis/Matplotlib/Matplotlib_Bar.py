import matplotlib.pyplot as plt
from random import random
n = 12
X = [ x for x in range(n)]
Y1 = [(1 - mx / float(n)) * random() for mx in X ]
Y2 = [-(1 - mx / float(n)) * random() for mx in X ]
print(type(Y1))
plt.bar(X, Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, Y2, facecolor='#ff9999', edgecolor='white')

for x, y in zip(X, Y1):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(x + 0.1, y + 0.05, '%.2f' % y, ha='center', va='bottom')

for x, y in zip(X, Y2):
    # ha: horizontal alignment
    # va: vertical alignment
    plt.text(x + 0.1, y - 0.05, '%.2f' % y, ha='center', va='top')

plt.xlim(-.5, n)
plt.xticks(())
plt.ylim(-1.25, 1.25)
plt.yticks(())

plt.show()
