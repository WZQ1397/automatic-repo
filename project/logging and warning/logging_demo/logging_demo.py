import logging
from logging.config import dictConfig

# 日志等级
# DEBUG < INFO < WARNING < ERROR < CRITICAL

FORMATTER_INFO = {
    'name': '%(name)s',
    'levelno': '%(levelno)s',
    'levelname': '%(levelname)s',
    'pathname': '%(pathname)s',
    'filename': '%(filename)s',
    'module': '%(module)s',
    'funcName': '%(funcName)s',
    'lineno': '%(lineno)d',
    'created': '%(created)f',
    'relativeCreated': '%(relativeCreated)d',
    'asctime': '%(asctime)s',
    'thread': '%(thread)d',
    'threadName': '%(threadName)s',
    'process': '%(process)d',
    'message': '%(message)s',
}

FORMATTER = logging.Formatter(f'{FORMATTER_INFO["asctime"]}: {FORMATTER_INFO["name"]}: {FORMATTER_INFO["levelname"]}: {FORMATTER_INFO["message"]}', datefmt='%Y-%m-%d %H:%M:%S %p')

def simple_using():
    # logging.basicConfig(level=logging.ERROR)
    logging.debug('debug text')
    logging.warning('warning text')
    logging.info('info text')
    logging.error('error text')
    logging.critical('critical text')

    # logger = logging.getLogger('root.first')
    # logger.debug('first warning text')
    # logger.warning('first waring text')
    # logger.info('first info text')
    # logger.error('first error text')
    # logger.critical('first critical text')

def file_name_demo():
    logging.basicConfig(filename='log.log')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def file_mode_demo():
    logging.basicConfig(filename='log.log', filemode='w')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def format_demo():
    logging.basicConfig(level=logging.DEBUG,format='%(name)s %(levelname)s: %(asctime)s: %(message)s')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def datefmt_demo():
    logging.basicConfig( level=logging.DEBUG, format='%(name)s %(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def style_demo():
    # % style
    # logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s: %(asctime)s: %(message)s', style='%')
    # logging.debug('debug text')
    # logging.info('info text')
    # logging.warning('warning text')
    # logging.error('error text')
    # logging.critical('critical text')

    # { style
    # logging.basicConfig(level=logging.DEBUG, format='{name} {levelname}: {asctime}: {message}', style='{')
    # logging.debug('debug text')
    # logging.info('info text')
    # logging.warning('warning text')
    # logging.error('error text')
    # logging.critical('critical text')

    # $ style
    logging.basicConfig(level=logging.DEBUG, format='$name $levelname: $asctime: $message', style='$')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def level_demo():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

def handles_demo():
    stream_handle = logging.StreamHandler()
    file_handle = logging.FileHandler(filename='handles.log')
    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handle, file_handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

class myFilter(logging.Filter):
    def filter(self, record):
        if record.levelno >= 30:
            return True
        else:
            return False

def filter_demo():
    stream_handle = logging.StreamHandler()
    stream_handle.addFilter(myFilter())
    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

# StreamHandler: 将日志输出到终端
def stream_handler_demo():
    logger = logging.getLogger('stream_handle')
    # 设置全局最低级别
    logger.setLevel(logging.DEBUG)

    # 设置handle
    stream_h = logging.StreamHandler()
    # 设置handler的最低级别
    stream_h.setLevel(logging.DEBUG)

    # 设置formatter
    stream_h.setFormatter(FORMATTER)

    logger.addHandler(stream_h)
    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')

# FileHandle: 将日志写入文件
def file_handle_demo():
    logger = logging.getLogger('file_handle')
    logger.setLevel(logging.DEBUG)

    file_h = logging.FileHandler('file_handle.log', mode='a', encoding='utf-8')
    file_h.setLevel(logging.DEBUG)

    file_h.setFormatter(FORMATTER)

    logger.addHandler(file_h)

    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')

class myHandle(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        sys.stderr.write(msg)

def my_handle_demo():
    logging.basicConfig(handlers=[myHandle()])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

class myFormatter(logging.Formatter):
    def format(self, record):
        return 'hello world\n'

def my_formatter_demo():
    handle = myHandle()
    handle.setFormatter(myFormatter())
    logging.basicConfig(handlers=[handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')

import sys
def sys_stderr_stdout_demo():
    sys.stdout.write('stdout1')
    sys.stdout.flush()
    sys.stderr.write('stderr1')
    sys.stdout.write('stdout2')
    sys.stdout.flush()
    sys.stderr.write('stderr2')
    # 显示效果：
    #   stdout1 stdout2 stderr1 stderr2
    # 因为stdout有缓存，而stderr没有缓存
    # 清除缓存的方法：
    # 1. 后面添加 \n
    # 2. 执行脚本时使用-u
    # 3. 使用sys.stdout.flush()方法

def dict_config_demo():
    config = {
        'version': 1,  # 这个参数只能为1，必选参数
        'incremental': False,  # 可选参数，默认为False。如果这里定义的对象已经存在，那么这里对这些对象的定义是否应用到已存在的对象上。值为False表示，已存在的对象将会被重新定义。
        'disable_existing_loggers': False,  # 可选参数，默认值为True。该选项用于指定是否禁用已存在的日志器loggers，如果incremental的值为True则该选项将会被忽略

        # 定义filters，每个键都为一个filter
        'filters': {
            # filter的名字，下面handle出会使用到
            'filter1': {
                # 必选项，构造filter的类，必须是logging.Filter或者其子类,而且必须为完整路径
                '()': 'logging.Filter',
            },
            'filter2': {
                '()': 'logging.Filter',
            },
        },
        # 定义的formatters
        'formatters': {
            # formatters的名称，handle处会使用到
            'formatter1': {
                # formatter的类，必选参数，必须为logging.Formatter或者其子类
                '()': 'logging.Formatter',
                # Formatter的format参数
                'format': '[{name}] {message}',
                # Formatter的style参数
                'style': '{',
                # Formatter的datefmt参数
                'datefmt': '%Y-%m-%d %H:%M:%S %p'
            }
        },
        # 定义handle
        'handlers': {
            # handle的名字，下面logger处使用
            'handle0': {
                # handle的level
                'level': 'INFO',
                # 指定handle的filter，这里的就是用到了上面的filter1
                'filters': ['filter1'],
                # 指定handle的class
                'class': 'logging.StreamHandler',
            },
            'handle1': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                # 指定formatter，上面的formatter1
                'formatter': 'formatter1',
            },
            'handle2': {
                'level': 'ERROR',
                'filters': ['filter1'],
                'class': 'logging.FileHandler',
                'filename':'dict.txt'
            }
        },
        'loggers': {
            # logger的name
            'logger1': {
                # 指定logger的handles
                'handlers': ['handle0', 'handle1'],
                # 指定logger的级别
                'level': 'ERROR',
                # 可选参数，是否将logger消息传递给parent logger,值为True或者False
                'propagate': False,
            },
            'logger2': {
                'handlers': ['handle2'],
                'level': 'INFO',
                # 可选参数，是否将logger消息传递给parent logger,值为True或者False
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['handle0', 'handle1'],
            'level': 'INFO',
        },
    }

    dictConfig(config=config)
    logger = logging.getLogger('logger1')
    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')


if __name__ == '__main__':
    dict_config_demo()
