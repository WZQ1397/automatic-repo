# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-01-30 20:17
'''
run_forever 完成任务调度: 3.7+后可能不支持
'''
from datetime import datetime
from asyncio import get_event_loop,gather
from subprocess import PIPE, Popen
from concurrent.futures import ThreadPoolExecutor
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
  pass


if __name__ == '__main__':
  # 启动协程
  loop_instance = get_event_loop()
  # 获取协程时间
  current_time = loop_instance.time()
  urllist = ["https://www.baidu.com", "https://www.python.org", "https://www.qq.com", "https://www.runoob.com"]

  exec = ThreadPoolExecutor(3)
  mytasks = []
  while urllist:
    task = loop_instance.run_in_executor(exec,download,urllist.pop(),current_time)
  mytasks.append(task)
  # 永久运行
  loop_instance.run_until_complete(gather(*mytasks))

