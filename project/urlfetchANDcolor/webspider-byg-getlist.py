from bs4 import BeautifulSoup
import lxml,html5lib
from urllib import request
import gzip,re

PATH = ''
header = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'}
main  = 'http://www.banyungong.org/'

def ungzip(data,url):
    try:
        print(url,"正在解压缩...")
        data = gzip.decompress(data)
        print(url,"解压完毕...")
    except:
        print(url,"未经压缩，无需解压...")
    return data

class BygResourceDownload(object):
    def __init__(self):
        #self.suburl = 'category/302-1.html'
        #self.url = main+suburl
        self.count = 0

    #从文档中找到所有<a>标签的内容
    def spiderbyg(self):
        for link in soup.find_all('a',class_='vTitle'):
            '''
            val = re.split('/',str(link.get('href'))) '''
            key = 'magnetm'

            '''
            if len(val) > 1:
                if val[1] == key:
            '''
            self.count += 1
            fmt = " No:",str(self.count),main + key + '/'+eval(str(re.split('/',str(link.get('href')))))[-1]
            fmt = " ".join(fmt)
            res = link.text,'\n',str(fmt)
            print(" ".join(res))
            with open(PATH+'byg.log','ab') as f:
                f.write(str(link.text+"\n").encode('GB18030'))
                f.write(str(fmt+'\n').encode('GB18030'))

    def weblist(self):
        req = request.Request(main,headers=header)
        res = request.urlopen(req)
        data = ungzip(res.read(),main)
        soup = BeautifulSoup(data,'html5lib')
        lst = {}
        for link in soup.find_all('option')[1:]:
            if link.get('value')[-2:] != '00' and link.get('value')[-2:] != '99':
                print(link.get('value'),link.text)
                lst[link.get('value')] = link.text
        return lst

if __name__ == '__main__':
    for ptype in BygResourceDownload().weblist():
        for var in range(1,2):
            suburl = 'category/'+str(ptype)+'-'+str(var)+'.html'
            url = main+suburl
            req = request.Request(url,headers=header)
            res = request.urlopen(req)
            data = ungzip(res.read(),url)
            #添加一个解析器
            soup = BeautifulSoup(data,'html5lib')
            BygResourceDownload().spiderbyg()
else:
    with open(PATH+'byg.db','r') as f:
            print(f.read())

#print(soup.title.name)
#print(soup.title.text)
# print(soup.body)

#从文档中找到所有文字内容
#print(soup.get_text())

'''
https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/index.html
'''