from bs4 import BeautifulSoup
from urllib import request
import gzip,re,time,os
from datetime import date

PATH = ''
REC_DATE=str(date.today())

#FIXME 8.24 503 pycharm is ok

header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36"}
main = 'http://gaoqing.la/'

def ungzip(data,url):
    try:
        #print(url,"正在解压缩...")
        data = gzip.decompress(data)
        #print(url,"解压完毕...")
    except:
        #print(url,"未经压缩，无需解压...")
        pass
    return data

def color(type):
    COLOR = {}
    COLOR['COLOR_GREEN'] = "\033[01;32m"
    COLOR['COLOR_RED'] = "\033[01;31m"
    COLOR['COLOR_YELLOW'] = "\033[01;33m"
    COLOR['COLOR_NONE'] = "\033[m"
    return COLOR[type]

class MovieInfoSpider():
    url = main
    req = request.Request(url,headers=header)
    res = request.urlopen(req)
    data = ungzip(res.read(),url)
    #添加一个解析器
    soup = BeautifulSoup(data,'html5lib')

    def judgefile_whether_exist(self,filepath):
        crush = 1 if os.path.exists(filepath) else print("NOEXIST! START!")
        print(filepath)
        if crush:
            choice = str(input(color('COLOR_RED')+"DO YOU WANT TO DELETE FILE?[y/N]"+color('COLOR_NONE')+":\n"))
            if choice.lower() == 'y' or choice.lower() == 'yes':
                os.remove(filepath)

    def getcontent(self):
        COUNT = 0
        reg = re.compile(r'magnet*?')
        FILE_PATH = PATH+"MOVIE-"+REC_DATE+".log"
        self.judgefile_whether_exist(FILE_PATH)
        for step in self.soup.find_all('a',class_="zoom"):
            req = request.Request(step.get('href'),headers=header)
            res = request.urlopen(req)
            data = ungzip(res.read(),step.get('href'))
            #print(data)
            time.sleep(5)
            part1 = "\nlink: "+step.get('href')+step.get('title')+"\n[img]"+str(step.img.get('src'))+"[/img]"
            soup = BeautifulSoup(data,'html5lib')
            for x in soup.find_all('div',attrs={'id':'post_content'}):
                part2 = x.text.replace('http://www.imdb.com/title',"http://1080pdy.com").replace('https://movie.douban.com/subject',"http://1080pdy.com").strip()
            part3 = ""
            for x in soup.find_all(href=reg):
                part3 += "Download:\n"+str(re.split(r'>',str(x))[0]).replace("<a href=\"","[hide][code]").replace("\"","[/code][/hide]")+"\n"

            content = str(part1+"\n"+part2+"\n"+part3+"\n\n"+"=+="*20+"\n")
            with open(FILE_PATH,'ab') as f:
                f.write(content.encode())

            COUNT += 1
            print(color('COLOR_GREEN')+"No:{:3d}.......OK".format(COUNT)+color('COLOR_NONE'))
            time.sleep(0.5)

MovieInfoSpider().getcontent()