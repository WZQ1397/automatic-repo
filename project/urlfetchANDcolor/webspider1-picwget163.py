from urllib import request
import re,os,threading

#定义文件保存路径
targetPath = "E:\\python\TMP\\"

def saveFile(path):
    #检测当前路径的有效性
    if not os.path.isdir(targetPath):
        os.mkdir(targetPath)

    #设置每个图片的路径
    pos = path.rindex('/')
    t = os.path.join(targetPath,path[pos+1:])
    return t

def reqfun(web):
    req = request.Request(url=web, headers=headers)
    res = request.urlopen(req)
    return res.read()
#用if __name__ == '__main__'来判断是否是在直接运行该.py文件


# 网址
url = "http://pp.163.com/square"
headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
           }


for link2,t2 in set(re.findall(r'(http://pp.163.com/[^\s]*?(html))', str(reqfun(url)))):
    if os.path.basename(link2).lower() == 'html':
        continue
    print(link2)

    for link,t in set(re.findall(r'(https?:[^s]*?(jpg|png|gif))', str(reqfun(link2)))):
       res = request.urlopen(link)
       if re.split("\.",os.path.basename(link))[1].lower() == 'gif' or len(res.read()) <10000:
           continue
       print(link)
       try:
           request.urlretrieve(link,saveFile(link))
       except:
           print('失败')