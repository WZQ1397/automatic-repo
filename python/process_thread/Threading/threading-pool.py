from concurrent.futures import ThreadPoolExecutor
import time,random,threading

lock=threading.Lock()
def func(n):
  ll,before_num,set_num = [],0,0
  # 获取锁
  lock.acquire()
  for x in range(20):
    before_num = random.randrange(n+1)
    #print("before_num:",before_num)
    set_num = before_num + set_num
    #print("set_num:",set_num)
    ll.append(set_num)
  print('{}.{}\n'.format(n,ll))
  # 释放锁
  lock.release()
  time.sleep(0.5)
  return ll


def tasks(num):
  # td = ThreadPoolExecutor(num)
  xraylist=[x for x in range(1,10,2)]
  # 使用上下文创建线程池
  with ThreadPoolExecutor(num) as td:
    # 将序列中的每个元素都执行同一个函数
    for v in td.map(func,xraylist):
      print(v)

tasks(5)
