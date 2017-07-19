from urllib import request
import re,os,threading,time,queue

q = queue.Queue(20480)

#定义文件保存路径
targetPath = "E:\\python\TMP\\"
class MyThread(threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.url = q.get()

    def run(self):
        print(self.url)
        for link,t in set(re.findall(r'(http://699pic.com/tupian[^\s]*?(html))', str(reqfun(self.url)))):
           #res = request.urlopen(link)
           #if re.split("\.",os.path.basename(link))[1].lower() == 'gif' or len(res.read()) <10000:
           #    continue
           #print(link)
           for piclink,t in set(re.findall(r'(http://seopic.699pic.com/photo/[^s]*?jpg[^s]*?(jpg))', str(reqfun(link)))):
                print(piclink,"loading...")
                try:
                    request.urlretrieve(piclink,self.saveFile(piclink))
                    time.sleep(1)
                    if os.path.exists(targetPath+os.path.basename(piclink)) is False:
                        request.urlretrieve(piclink,self.saveFile(piclink))
                        print("err")
                except:
                    print('失败')
        q.task_done()

    def saveFile(self,path):
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
headers = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }

print("START".center(50,"-"))


def main_function():
    threads_num = 10
    i = 1
    while True and i < 400:
        for j in range(threads_num):
            x = i + j
            q.put('http://699pic.com/backgrounds-'+str(x)+'-0-0-0.html')
            myThread = MyThread()
            myThread.setDaemon(False)
            myThread.start()
            print(j)
        q.join()

        i = i+j
        time.sleep(10)

main_function()