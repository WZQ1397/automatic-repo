# python day 25
# author zach.wang
# -*- coding:utf-8 -*-
import logging,platform
#TODO 不分割日志

PATH = 'D:\\' if platform.system() == 'Windows' else '/var/log'
LOG_FILENAME = PATH+'logging_example.out'
#level 为最低标准，只记录高于制定级别日志
logging.basicConfig(level=logging.ERROR,
                    format='%(levelname)s %(asctime)s :FILE: %(filename)s [line:%(lineno)d]  %(message)s',
                    datefmt='%c',
                    filename=LOG_FILENAME)

logging.debug('调试信息')
logging.info('有用的信息')
logging.warning('警告信息')
logging.error('错误信息')
logging.critical('严重错误信息')
with open(LOG_FILENAME, 'rt') as f:
    body = f.read()

print(body)

#关闭日志，并将所有内容写入到磁盘中
logging.shutdown()