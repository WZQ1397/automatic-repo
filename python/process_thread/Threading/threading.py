import threading as td
from queue import Queue
from datetime import datetime
import time

def get_td_args(num):
  for _ in range(num):
    act_td = "Active: {}".format(td.active_count())
    all_td = "All: {}".format(td.enumerate())
    cur_td = "Current thread:{}".format(td.current_thread().name)
    main_td = "Main thread:{}".format(td.main_thread)
    arglist = [act_td,all_td,cur_td,main_td]
    time.sleep(0.5)
    for v in arglist:
      print(v)
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def new_job(num,q):
  startTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
  print("doing sth...")
  for _ in range(num):
    end = get_td_args(_)
  # 把要返回的值放入队列, 多线程不支持return返回, 需要使用队列通信
  q.put((startTime,"==>",end))
  
def add_td_byorder(curr,num):
  '''
  实现按顺序执行的多线程
  '''
  added_td = td.Thread(target=new_job,name="zach-{}".format(num),args=(num,))
  added_td.start()
  # 确认任务完成后再执行后面的
  # added_td.join()
  print("task {} end!".format(curr))

def add_td_inAsync(num)->list:
  '''
  实现异步多线程
  '''
  q = Queue()
  tdList,result=[],[]
  for curr in range(num):
    added_td = td.Thread(target=new_job,name="zach-{}".format(num),args=(num,q))
    added_td.start()
    # 把任务保存到列表中
    tdList.append(added_td)
  # 实现异步执行
  for t in tdList:
    t.join()
  # 获取队列中的值放到空列表中
  for _ in range(num):
    result.append(q.get())
  return result
  
def start_jobs(num=5):
  # for _ in range(num):
    # add_td_byorder(_,num)
  res = add_td_inAsync(num)
  print(res)

start_jobs()
    
#add_td(num=5)
