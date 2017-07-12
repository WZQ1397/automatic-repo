from urllib import request
import random,platform,os
from bs4 import BeautifulSoup

PREFIX = "ceph"
path = ""
if path == "":
    if platform.system() == "Windows":
        path = os.getcwd()+"\\"
    else:
        path = os.getcwd()+"/"

filepath = path+PREFIX+".html"

def saveFile(data):
    #TODO SELECT SINGLE FILE OR MULT FILE

    file = open(filepath,'wb')
    #将博文信息写入文件(以utf-8保存的文件声明为gbk)
    for d in data:
        file.write(d.encode('GB18030'))
    file.close()

url = 'http://blog.csdn.net/junming_zhao/article/details/72528533'
user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
               'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
               'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
               'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
               'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
               'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

index=random.randint(0, 9)
user_agent=user_agents[index]
headers={'User_agent':user_agent}

req = request.Request(url=url, headers=headers)
page = request.urlopen(req)
# 从我的csdn博客主页抓取的内容是压缩后的内容，先解压缩
data = page.read()
data = data.decode('utf-8')
# 得到BeautifulSoup对象
soup = BeautifulSoup(data,'html5lib')
title = str(soup.find(class_='link_title').text).strip()
print(title)
content = str(soup.find('div',class_='article_content tracking-ad'))
print(content)
saveFile(title+"<br/><br/>"+content)