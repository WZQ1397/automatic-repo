from bs4 import BeautifulSoup
from urllib import request
import gzip,re,time,os

header = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'}

def ungzip(data,url):
    try:
        data = gzip.decompress(data)
    except:
        pass
    return data
url = 'http://www.cnblogs.com/lasgalen/p/4512755.html'
#reg = re.compile(r'magnet*?')
req = request.Request(url,headers=header)
res = request.urlopen(req)
data = ungzip(res.read(),url)
soup = BeautifulSoup(data,'html5lib')
for x in soup.find_all('div',attrs={'id':'cnblogs_post_body'}):
    #TODO cnblogs.cn     --> 'div',attrs={'id':'cnblogs_post_body'}
    #TODO blog.51cto.com --> 'div',class_='showContent'
    #TODO bbs.51cto.com  --> 'div',attrs={'id':'ad_thread4_0'}/'div',attrs={'class':'showContent'}
    #TODO blog.sina.com.cn/s --> 'div',attrs={'id':'sina_keyword_ad_area2'}
    #TODO blog.itpub.net --> 'div',class_='Blog_wz1'
    print(x)

    with open(os.path.basename(url),'wb') as f:
        f.write(str(x).encode())
