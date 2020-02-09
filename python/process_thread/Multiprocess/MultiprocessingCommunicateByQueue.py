from multiprocessing import Process, Queue
import os, time, random
#多进程通信queue
def write(q):
  for value in ['A', 'B', 'C']:
    print ('Put %s to queue...' % value)
    q.put(value)
    time.sleep(random.random())

def read(q):
  while True:
    value = q.get(True)
    print ('Get %s from queue.' % value)
    
if __name__ == '__main__':
  q = Queue()
	# 只有一个元素时, args赋值的元祖需要加逗号
  pw = Process(target=write, args=(q,))
  pr = Process(target=read, args=(q,))
  pw.start()
  pr.start()
  pw.join()
  pr.terminate()
