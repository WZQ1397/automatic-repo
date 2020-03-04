from multiprocessing import Process,Lock,Value
from multiprocessing import freeze_support
import time

def job(v, num, l):
    #l.acquire()
    print(v.value,num,l)
    for _ in range(10):
      time.sleep(0.1)
      v.value += num
      print(v.value)
    #l.release()

def multicore():
  freeze_support()
  l = Lock()
  #v = Value('i', 0)
  v=10
  p1 = Process(target=job, args=(v, 1, l))
  p2 = Process(target=job, args=(v, 3, l))
  p1.start()
  p2.start()
  p1.join()
  p2.join()

multicore()
