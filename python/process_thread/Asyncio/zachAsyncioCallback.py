# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-01-30 20:17
'''
ensure_future 和 create_task 完成任务调度: 推荐
add_done_callback 执行完成后的任务，如: 任务完成发送通知
'''
from datetime import datetime
from asyncio import get_event_loop,ensure_future
from subprocess import PIPE, Popen
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(message)s',
                    datefmt='%c')
def msgStdout(filename):
  msg = ""
  logging.info("{:=^50}".format(filename))
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


def runTime(startDate,looptime,fun):
  return  "Start:{}[{}] ==> Method:{}".format(startDate,looptime,fun)

def download(url,looptime,msg="",signal=[]):
  filename="D:\\{}.html".format(str(url).split('.')[-2].split('/')[-1])
  logging.info(runTime(datetime.now(),looptime,download.__name__))
  stdout = Popen("curl {} > {}".format(url,filename),stdout=PIPE,stderr=PIPE,universal_newlines=True, shell=True)
  logging.info("Endtime:{} [{}]: {}".format(datetime.now(),
                                            'ok' if stdout.returncode is None else stdout.returncode,                                        stdout.args.split()[1]))
  msgStdout(filename)

async def mytasks(urllist):
  try:
    [download(url,current_time) for url in urllist]
  except Exception as e:
    return e
  else:
    return f"[{len(urllist)} tasks complete!]"

def callback(startTime,endTime,future):
  logging.warning(f'{startTime} --> {endTime}')
  return "ok"

if __name__ == '__main__':
  startTime = datetime.now()
  # 启动协程
  loop_instance = get_event_loop()
  # 获取协程时间
  current_time = loop_instance.time()
  urllist = ["https://www.baidu.com","https://www.python.org","https://www.qq.com","https://www.runoob.com"]

  # 方法一: 使用create_task来创建任务，需要和async关键词配合使用
  # dw = loop_instance.create_task(mytasks(urllist))
  # 方法二: 使用ensure_future来创建任务，需要和async关键词配合使用
  dw = ensure_future(mytasks(urllist))
  # 在任务完成后回调任务(不带参数)
  # dw.add_done_callback(callback)

  # 在任务完成后，带参数的回调任务，需要使用偏函数，这里导入
  from functools import partial
  # partial(函数名,[arg1,arg2,...]) ,偏函数出入的参数在函数定义中需要在future默认回调参数之前
  dw.add_done_callback(partial(callback,startTime,datetime.now()))
  loop_instance.run_until_complete(dw)
  # 输出async关键词修饰的函数的返回结果
  logging.info(dw.result())

