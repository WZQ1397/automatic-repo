# python day 25
# author zach.wang
# -*- coding:utf-8 -*-
import logging
#TODO 使用配置文件
PROCESSNAME = 'zach'

zachlog = logging.getLogger(PROCESSNAME)

# Log some messages
def log():
    zachlog.debug('zach \t调试信息')
    zachlog.info('zach \t 有用的信息')
    zachlog.warning('zach \t 警告信息')
    zachlog.error('zach \t 错误信息')
    zachlog.critical('zach \t 严重错误信息')
