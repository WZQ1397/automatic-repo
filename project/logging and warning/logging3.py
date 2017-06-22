# python day 25
# author zach.wang
# -*- coding:utf-8 -*-
import logging,platform
from logging import config
#TODO 使用配置文件
PROCESSNAME = 'xyc'
#PATH = 'D:\\' if platform.system() == 'Windows' else '/var/log'
#LOG_FILENAME = PATH+PROCESSNAME
logging.config.fileConfig("logging_file.conf")

zachlog = logging.getLogger(PROCESSNAME)

import logging3_sub
# Log some messages
for i in range(500):
    zachlog.debug('调试信息')
    zachlog.info('有用的信息')
    zachlog.warning('警告信息')
    zachlog.error('错误信息')
    zachlog.critical('严重错误信息')
    logging3_sub.log()
