import gevent
"""
自动档的协程
自上而下从0开始计数，如果计数不大于sleep数，则跳过后面代码
否则，执行后面代码
"""
 
def run1():
    print("run1->1")
    gevent.sleep(2)
    print("run1->2")
 
def run2():
    print("run2->1")
    gevent.sleep(3)
    print("run2->2")
 
def run3():
    print("run3->1")
    gevent.sleep(1)
    print("run3->2")
 
def run4():
    print("run4->1")
    gevent.sleep(0)
    print("run4->2")
 
#由上而下依次执行
gevent.joinall([
    gevent.spawn(run1),
    gevent.spawn(run2),
    gevent.spawn(run3),
    gevent.spawn(run4),
])
