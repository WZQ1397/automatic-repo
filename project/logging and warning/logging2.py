# python day 25
# author zach.wang
# -*- coding:utf-8 -*-
import logging,platform,warnings
from logging import handlers
#TODO 分割日志
PROCESSNAME = 'zach'
PATH = 'D:\\' if platform.system() == 'Windows' else '/var/log'
LOG_FILENAME = PATH+PROCESSNAME+'.log'
zachlog = logging.getLogger()
zachlog.setLevel(logging.DEBUG)

fmt = '%(levelname)s\t %(asctime)s :FILE: %(filename)s [line:%(lineno)d]  %(message)s'
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1000,
    backupCount=5,
)

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(LOG_FILENAME)    # 获取名为tst的logger
zachlog.addHandler(handler)

def logwarning():
    warnings.warn('This warning is sent to the logs',DeprecationWarning)
    warnings.warn('After the warning')
    warnings.warn('This is a warning!')
    warnings.warn('This is a warning!')
    warnings.warn('This is a warning!')

# Log some messages
for i in range(20):
    #捕捉警告
    logging.captureWarnings(True)
    #重复的只执行一次
    warnings.simplefilter('once',UserWarning)
    #忽略所有警告
    #warnings.simplefilter("ignore")
    logwarning()
    zachlog.debug('调试信息')
    zachlog.info('有用的信息')
    zachlog.warning('警告信息')
    zachlog.error('错误信息')
    zachlog.critical('严重错误信息')

#TODO 状态-1 直接Trackback ERROR
#warnings.simplefilter('error', UserWarning)

#关闭日志，并将所有内容写入到磁盘中
logging.shutdown()
