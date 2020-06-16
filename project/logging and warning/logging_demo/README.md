# python logging模块的使用

logging模块主要是方便我们用来记录日志信息的，下面将列出logging模块的使用。

### 了解logging中的等级
|LEVEL|value|describe|
|:---:|:---:|:---:|
|NOTEST|0|不设置级别，按照父logger的级别显示日志，如果是root logger，那么就会显示所有的日志|
|DEBUG|10|程序的详细debug信息，调试代码会用到|
|INFO|20|确定程序是否按照正常的运行|
|WARNING|30|程序发出警告，但是还能正常运行|
|ERROR|40|程序发生错误，无法运行程序|
|CRITICAL(FATAL)|50|程序出现致命错误，无法运行|

### 简单使用

```python
import logging

def simple_using():
    logging.debug('debug text')
    logging.warning('warning text')
    logging.info('info text')
    logging.error('error text')
    logging.critical('critical text')
```
上面的代码只会在控制台显示3条信息
```text
WARNING:root:warning text
ERROR:root:error text
CRITICAL:root:critical text
```
这是因为logging默认的`LEVEL`是`WARNING`,logging只会显示级别大于等于`WARNING`的日志信息。所以这里就只会显示这样三条。当然，我们也可以改变LEVEL。

### logging.basiConfig函数

这个函数是用来配置root logger的参数的。

1. filename: 指定日志文件的文件名。所有会显示的日志都会存放在这个文件中去
```python
def file_name_demo():
    # 只有日志级别大于等于INFO的，才会被写入log文件中
    logging.basicConfig(filename='log.log')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```
运行这段函数，在当前目录下就会生成一个log.log的文件，里面会写入下面几条信息。
```text
WARNING:root:warning text
ERROR:root:error text
CRITICAL:root:critical text
```

2. filemode: 文件的打开方式，默认是`a`,也就是追加
```python
def file_mode_demo():
    logging.basicConfig(filename='log.log', filemode='a')
    # logging.basicConfig(filename='log.log', filemode='w')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```
也就是每次写入日志都是添加到文件最后面，如果设置为`w`,那么每次写入都会从头开始写入，就会覆盖前面的日志。

3. format: 指定显示日志的信息格式。

首先给出所有的日志格式

##### 日志格式

|语法|释义|
|:---:|:---:|
|%(name)s|logger的名字|
|%(levelno)s|数字形式的日志级别|
|%(levelname)s|文本形式的日志级别|
|%(pathname)s|调用日志输出函数的模块的完整路径名，可能没有|
|%(filename)s|调用日志输出函数的模块的文件名|
|%(module)s|调用日志输出函数的模块名|
|%(funcName)s|调用日志输出函数的函数名|
|%(lineno)d|调用日志输出函数的语句所在的代码行|
|%(created)f|LogRecord的创建时间，也就是当前时间，time.time()|
|%(msecs)d|LogRecord的创建时间的毫秒部分|
|%(relativeCreated)d|输出日志信息的，自logger创建以来的毫秒数|
|%(asctime)s|字符窜形式的当前时间，默认格式为"2003-07-08 19:30:43, 896", 都好后面是毫秒|
|%(thread)d|线程ID，可能没有|
|%(threadName)s|线程名，可能没有|
|%(process)d|进程ID，可能没有|
|%(message)s|用户输出的消息|

```python
def format_demo():
    logging.basicConfig(level=logging.DEBUG,format='%(name)s %(levelname)s: %(asctime)s: %(message)s')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

显示信息为:
```text
root DEBUG: 2019-09-05 16:01:01,746: debug text
root INFO: 2019-09-05 16:01:01,759: info text
root WARNING: 2019-09-05 16:01:01,759: warning text
root ERROR: 2019-09-05 16:01:01,759: error text
root CRITICAL: 2019-09-05 16:01:01,759: critical text
```

4. datefmt: 指定日期的显示格式
```python
def datefmt_demo():
    logging.basicConfig( level=logging.DEBUG, format='%(name)s %(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p')
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

##### python 中日期格式化符号
|符号|描述|
|:---:|:---:|
|%y|两位数的年份表示 (00-99)|
|%Y|四位数的年份标书|
|%m|月份（01-12）|
|%d|天（0-31）|
|%H|24小时制小时数（01-23）|
|%I|12小时制小时数（01-12）|
|%M|分钟（00-59）|
|%S|秒数（00-59）|
|%a|本地简化星期名称|
|%A|本地完整星期名称|
|%b|本地简化月份名称|
|%B|本地完整月份名称|
|%c|本地相应的日期表示和时间表示|
|%j|年内的一天（001 - 366）|
|%p|本地AM或PM的等价符|
|%U|一年中的星期数（00-53），星期天为星期的开始|
|%W|一年中的星期数（00-53），星期一为星期的开始|
|%w|星期（0-6），星期天为星期的开始|
|%x|本地相应的日期表示|
|%X|本地相应的时间表示|
|%Z|当前时区的名称|
|%%|%号本身|

5. style: 指定格式化风格

有三种风格：%, {, $, 默认就是%这种,下面给出了三种风格的使用方法

```python
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
```

6. level: 配置level，低于这level的日志将不会被显示或存储。高于或等于才会被存储
```python
def level_demo():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

7. handles: 指定handles，可以多个
```python
def handles_demo():
    # 将日志输出到终端的handle
    stream_handle = logging.StreamHandler()
    # 将日志输出到handles.log文件中的log
    file_handle = logging.FileHandler(filename='handles.log')
    
    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handle, file_handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```
handle是什么？

每条会显示的日志信息都会交给handle处理，由handle决定将日志存放到哪里，怎样存放。

所以上面的日志信息既会在终端显示也会存放到handles.log文件中。

### logging.Logger对象的使用

在一个项目中，我们可能根据不同的情况打印不同的日志，这样的话我们就需要多个日志模型。而我们前面一直使用logging明显不够用了。这个时候我们就需要使用logger对象了。其实前面我们直接使用logging.debug这些的时候，使用的也是一个logger对象，这是root logger。也就是根logger，我们自己新建的logger，其实都是root logger 的子logger，如果没有设置level的话，就会使用父logger的level。

`logging.getLogger([name])`: 得到一个Logger对象

* 返回一个logger实例，如果没有指定name，返回root logger
* 只要name相同，返回的logger实例就是同一个而且只能有一个，name和logger实例是一一对应的，这意味着，无须把logger实例在各个模块中传递，只要只掉name，就能得到同一个logger实例。
* logger是一个树形层级结构，在使用接口debug，info，warn，error，critical之前必须创建Logger实例，即创建一个记录器，如果没有显式的进行创建，则默认创建一个root logger，并应用默认的日志级别(WARN)，处理器Handler(StreamHandler，即将日志信息打印输出在标准输出上)，和格式化器Formatter(默认的格式即为第一个简单使用程序中输出的格式)。
* 创建Logger实例后，可以使用以下方法进行日志级别设置，增加处理器Handler。 

`logger.setLevel(logging.ERROR)` : 设置日志级别为ERROR，即只有日志级别大于等于ERROR的日志才会输出 
`logger.addHandler(handler_name)` : 为Logger实例增加一个处理器
`logger.removeHandler(handler_name)` : 为Logger实例删除一个处理器

剩下的用法就和logging.debug，logging.info。。。这些用法一样了，只不过我们需要将logging改成logger

### logging.Handle对象使用

内置handle的使用
1. StreamHandle: 传入一个流对象，默认是`sys.stderr`。将日志输出到传入的流中

sys.stderr：输出信息到终端

```python
def stream_handler_demo():
    logger = logging.getLogger('stream_handle')
    # 设置logger的全局最低级别
    logger.setLevel(logging.DEBUG)

    # 设置handle
    stream_h = logging.StreamHandler()
    # 设置handler的最低级别
    stream_h.setLevel(logging.DEBUG)
    logger.addHandler(stream_h)
    
    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')
```

上面的信息就会被打印在终端显示

2. FileHandle: 将日志信息存放在文件中
```python
def file_handle_demo():
    logger = logging.getLogger('file_handle')
    logger.setLevel(logging.DEBUG)

    file_h = logging.FileHandler('file_handle.log', mode='a', encoding='utf-8')
    file_h.setLevel(logging.DEBUG)
    logger.addHandler(file_h)

    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')
```

其实FileHandle底层也是使用的StreamHandle，传入了一个文件流进入。

### logging.Formatter对象使用

和logging.basicConfig中参数配置format的参数一样。

* fmt: 指定日志显示的样式
* datefmt: 指定日志中时间的显示样式
* style: 日志的风格，有三种，和basicConfig中一样。
```python
import logging
def formatter_demo():
    logger = logging.getLogger('formatter')
    logger.setLevel(logging.DEBUG)

    file_h = logging.FileHandler('formatter.log', mode='a', encoding='utf-8')
    file_h.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s %(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p', style='%')
    file_h.setFormatter(formatter)

    logger.addHandler(file_h)

    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')
```

### logging.Filter对象的使用

logging.filter可以对日志信息进行过滤，让我们完成更复杂的存储。

首先我们定义一个myFilter类，继承自logging.Filter类。然后重写filter方法。

filter方法：
* record：一个logging.LogRecord对象，包含了日志中的所有信息
* 如果我们想把这条日志交给handle处理，也就是显示这条日志信息，就返回1（True），否则就返回0（False）。

```python
class myFilter(logging.Filter):
    def filter(self, record):
        if record.levelno >= 30:
            return True
        else:
            return False

def filter_demo():
    # 生成handle
    stream_handle = logging.StreamHandler()
    # 生成filter
    filter = myFilter()
    # handle中添加filter
    stream_handle.addFilter(filter)
    
    # 使用root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

也就是说，所有的日志都会先经过filter，再交给handle处理，我们就可以在filter中做一些过滤条件了。

### 自定义Handle

有时候python自带的handle满足不了我们的需求，现在我的版本是python3.7,就只有一个StreamHandle和FileHandle这两个handle，但是在实际开发中，他们是远远满足不了我们的需求的，所以我们就可以自定义handle。

自定义handle我们只需要注意两个点。
1. 继承自logging.Handle
2. 编写emit函数，所有的操作都是在emit函数中完成的

```python
class myHandle(logging.Handler):
    def emit(self, record):
        # 为了方便我们查看效果，这里我就打印了一下30个*     
        print("*"*30)
        print(record)

def my_handle_demo():
    # 给root logger添加我们自定义的handle
    logging.basicConfig(handlers=[myHandle()])
    
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

### 自定义Formatter

自定义Formatter我们需要注意下面几点：
1. 继承自logging.Formatter
2. 编写format方法
3. 一般都会在handle的emit中使用我们的Formatter

```python
import logging
import sys

class myHandle(logging.Handler):
    def emit(self, record):
        # 在这里我们可以使用self.format()方法得到我们定义的myFormatter中的format方法.
        msg = self.format(record)
        sys.stderr.write(msg)
        
class myFormatter(logging.Formatter):
    def format(self, record):
        return 'hello world\n'

def my_formatter_demo():
    # 生产handle
    handle = myHandle()
    # 给handle设置formatter
    handle.setFormatter(myFormatter())
    # 给root logger 添加handle
    logging.basicConfig(handlers=[handle])
    logging.debug('debug text')
    logging.info('info text')
    logging.warning('warning text')
    logging.error('error text')
    logging.critical('critical text')
```

### root logger 和 其他logger 的关系
* 如果不创建logger实例， 直接调用logging.debug()、logging.info()logging.warning()、logging.error()、logging.critical()这些函数， 那么使用的logger就是 root logger， 它可以自动创建，也是单实例的。
* 通过logging.getLogger()或者logging.getLogger('')得到root logger实例。
* root logger默认的level是logging.WARNING
* logger的name的命名方式可以表示logger之间的父子关系. 
    比如：parent_logger = logging.getLogger('foo')
        child_logger = logging.getLogger('foo.bar')
* logger有一个概念，叫effective level。 如果一个logger没有显示地设置level，那么它就用父亲的level。如果父亲也没有显示地设置level， 就用父亲的父亲的level，以此推….最后到达root logger，一定设置过level。默认为logging.WARNING,child loggers得到消息后，既把消息分发给它的handler处理，也会传递给所有祖先logger处理，


### logging.config.dictConfig的使用

我们看到这个函数的名字我们也能大概猜到这个函数是干嘛的。从dict中读取logger的配置
```python
from logging.config import dictConfig
import logging
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

    # 使用配置创建logger
    dictConfig(config=config)
    # 得到logger1这个logger
    logger = logging.getLogger('logger1')
    
    logger.debug('debug text')
    logger.info('info text')
    logger.warning('warning text')
    logger.error('error text')
    logger.critical('critical text')
```

上面，我们就通过dict来配置了logger，一般这种方法也是最常用的

**总结：**
1. 打印日志需要日志模型logger
2. logger中我们可以配置handle， formatter， filter
3. 日志的信息先后到达顺序为 filter -> handle -> formatter -> handle（先到达filter中，然后到达handle中，在handle中调用formatter，然后又回到handle中）
