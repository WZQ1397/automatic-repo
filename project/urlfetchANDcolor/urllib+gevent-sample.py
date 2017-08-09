# python day 18
# author zach.wang
# -*- coding:utf-8 -*-
import gevent
from gevent import monkey
from urllib.request import urlopen

#防止IO阻塞
monkey.patch_all()

dir = "E:\python\\urlfetch\\"
def trapurl(url):
    res = urlopen(url)
    data = res.read()
    webname = "".join(("".join(url.split("//")[1:])).split("/")[:1])
    #需要使用二进制写入，否则无法换行
    with open(dir+webname+".html","wb") as f:
        f.write(data)
    gevent.sleep(1)
    print("{} fetch success!".format(webname))

#限制UTF-8编码
gevent.joinall([gevent.spawn(trapurl,"https://www.python.org/"),
               gevent.spawn(trapurl,"http://hukumusume.com/douwa/koe/aesop/09/05.htm"),
                gevent.spawn(trapurl,"https://pymotw.com/3/py-modindex.html"),
                gevent.spawn(trapurl,"http://ava.qq.com/act/a20090522honor/index.htm"),
                gevent.spawn(trapurl,"http://lixian.xunlei.com/login.html"),])