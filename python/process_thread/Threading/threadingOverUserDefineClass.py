# coding:utf-8
import threading
import time

def timecounter(status):
	signal = "endTime" if status else "startTime"
	print("{}: {}".format(signal,time.ctime()))
	
# 从Thread继承，并重写run()
class MyThread(threading.Thread):
  def __init__(self,arg):
    super(MyThread, self).__init__() #注意：一定要显式的调用父类的初始化函数。
    self.arg=arg
  def run(self): #定义每个线程要运行的函数
    time.sleep(1)
    print('the arg is:%s\r' % self.arg)

# Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法。
timer = threading.Timer(1, timecounter,args=(0,))
timer.start()
for i in xrange(4):
	# 初始化自定义线程类
  t = MyThread(i)
	# 设置线程名
	t.setName('MyThread-%d' %i)
  t.start()
	# 判断线程是否还存在
	if t.isAlive():
		# 获取线程名
		print(t.get())

print('main thread end!')