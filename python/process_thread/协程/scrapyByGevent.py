import gevent, time
 
# from gevent import monkey
# monkey.patch_all()
 
from urllib import request
"""
利用协程，高效爬取网页
gevent模块默认不识别urllib的IO操作，
需要导入monkey给urllib里面的操作打上标记
"""
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
filename = "./result.html"
#爬取网页内容到本地
def get_url_content(url):
    print("GET: %s" % url)
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read()
    with open(url.split('.')[-2].split('/')[-1]+".html", "wb") as f:
        f.write(html)
    print("%d bytes received from %s" % (len(html), url))
    print("----------------------")
 
url_list = [
    "https://www.python.org/",
    "https://github.com/",
    "https://www.bilibili.com/"
]
 
#启动时间
serial_start_time = time.time()
#串行的方式获取网页内容
for url in url_list:
    get_url_content(url)
#计算花费时间
print("serial cost:", time.time() - serial_start_time)
 

#启动时间
async_start_time = time.time()
#并行的方式获取网页内容
gevent.joinall([
    gevent.spawn(get_url_content, "https://www.python.org/"),
    gevent.spawn(get_url_content, "https://github.com"),
    gevent.spawn(get_url_content, "https://www.bilibili.com/"),
])
#计算花费时间
print("async cost:", time.time() - async_start_time)
