from multiprocessing import Process,Pool
import time,os

content = [chr(ord('A')+x) for x in range(0,10)]

def fun_p(x):
  time.sleep(1)
  print(x,__name__,os.getpid())
  #TODO return value to callback
  return x

def end(x):
  """
  function end is a parent pid
  :param x: fun_p(pid) return to ppid
  """
  str_line = "-"*10
  print("{3}--{2}:{0} {1} {0}".format(str_line,time.ctime(),os.getpid(),x))

if __name__ == '__main__':
  pool = Pool(5)
  count = 0
  method = input("choose method SYNC or ASYNC\n:>")
	# 使用map方法
	# res = pool.map(fun_p,content)
	# print(count,res.get())

  for x in content:
    if method == "S".lower():
      #A--B--C--D
      res = pool.apply(fun_p,args=(x,))
    if method == "A".lower():
      #A--B-->
      #   C-->
      #   D-->
      res = pool.apply_async(fun_p, args=(x,),callback=end)
		print(count,res.get())
    count = count + 1

  print(count,__name__,os.getpid())
  pool.close()
  pool.join()
