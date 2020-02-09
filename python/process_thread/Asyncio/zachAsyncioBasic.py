# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-01-30 20:17
'''
run_forever 完成任务调度: 3.7+后可能不支持
'''
from datetime import datetime
from asyncio import get_event_loop
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
                                            'ok' if stdout.returncode is None else stdout.returncode,
                                            stdout.args.split()[1]))
  msgStdout(filename)

async def tasks(*args):
  # 获取协程时间
  current_time = loop_instance.time()
  # call_at(时间，函数名, [arg1,arg2,...])  指定时间启动
  loop_instance.call_at(current_time+1,download,"https://www.baidu.com",current_time)
  # call_soon(函数名, [arg1,arg2,...])  马上启动
  loop_instance.call_soon(download,"https://www.python.org",current_time)
  # call_later(顺序，函数名, [arg1,arg2,...]) 基于顺序先后启动
  loop_instance.call_later(2,download,"https://www.qq.com",current_time)
  loop_instance.call_later(1,download,"https://www.runoob.com",current_time)

if __name__ == '__main__':
  # 启动协程
  loop_instance = get_event_loop()
  # stop() 停止异步
  loop_instance.call_soon(lambda loop: loop.stop() , loop_instance)
  # 永久运行
  loop_instance.run_forever()

