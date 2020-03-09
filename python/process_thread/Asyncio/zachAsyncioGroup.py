# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-01-30 20:17
'''
run_until_complete 和 async 完成任务调度: 推荐
'''
from datetime import datetime
from asyncio import get_event_loop,wait,gather,Task
from subprocess import PIPE, Popen
from os.path import isfile
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(message)s',
                    datefmt='%c')
def msgStdout(filename):
  msg = ""
  logging.info("{:=^50}".format(filename))
  # 判断文件是否存在
  while not isfile(filename):
    pass
  else:
    with open(filename,'rb') as f:
      for v in f.readlines():
        try:
          msg = msg + v.decode('utf-8')
        except UnicodeDecodeError:
          msg = msg + v.decode('gbk')
        finally:
          if len(msg) >2:
            if msg[-1] == ">":
              logging.info(msg.strip(" &"))
              msg = ""
  return 0

def runTime(startDate,looptime,fun):
  return  "Start:{}[{}] ==> Method:{}".format(startDate,looptime,fun)

# 使用异步模式 run_until_complete必须与此结合使用
async def download(url,looptime,msg="",signal=[]):
  filename="D:\\{}.html".format(str(url).split('.')[-2].split('/')[-1])
  logging.info(runTime(datetime.now(),looptime,download.__name__))
  stdout = Popen("curl {} > {}".format(url,filename),stdout=PIPE,stderr=PIPE,universal_newlines=True, shell=True)
  logging.info("Endtime:{} [{}]: {}".format(datetime.now(),
                                            'ok' if stdout.returncode is None else stdout.returncode,
                                            stdout.args.split()[1]))
  msgStdout(filename)

if __name__ == '__main__':
  # 启动协程
  loop_instance = get_event_loop()
  # 获取协程时间
  current_time = loop_instance.time()
  urllist = ["https://www.baidu.com","https://www.python.org","https://www.qq.com","https://www.runoob.com"]
  # 创建任务生成器
  tasks = [download(url,current_time) for url in urllist]
  # run_until_complete(wait([列表])) 只要任务完成就停止
  # loop_instance.run_until_complete(wait(tasks))
  # gather(*列表名) 注意要加*, 使其能传入列表中的参数，而不是列表
  # loop_instance.run_until_complete(gather(*tasks))

  '''
  gather 与 wait 区别
  两者相似，但gather更高级，推荐
  例如下面对其分组
  '''
  group1 = tasks
  group2 = [download('http://www.verycd.com',current_time)]
  # 方法一: 直接使用
  # loop_instance.run_until_complete(gather(*group1,*group2))
  # 方法二: 封装后使用
  group1=gather(*group1)
  group2=gather(*group2)
  # 取消某个组执行
  # group1.cancel()
  # 封装后不再需要加*来修饰
  from concurrent.futures import CancelledError,BrokenExecutor,TimeoutError
  try:
    loop_instance.run_until_complete(gather(group1,group2))
  except CancelledError as e:
    logging.error("some tasks stoped!")
  except BrokenExecutor as e:
    raise Exception("Task start failed!")
  except TimeoutError as e:
    raise Exception("Too many times to exec,Timeout!")
  except KeyboardInterrupt as e:
    # 获取所有的任务
    all_tasks = Task.all_tasks()
    for task in all_tasks:
      # 停止所有任务
      task.cancel()
      logging.warning(f"{task.print_stack()} cancelled by user!")
    # loop_instance.stop()
    # loop_instance.run_forever()
  finally:
    # 查看异步调用函数返回结果
    try:
      logging.info(group1.result())
    except Exception:
      pass
    # 查看是否任务取消
    logging.warning("group1 cancelled!") if group1.cancelled() else logging.info("group1 executed!")
    # 查看任务是否完成
    logging.error("group1 run failed!") if group1.done() else logging.info("group1 success!")



