import gzip
def defeatblock(i):
    headers=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
             'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
             'IBM WebExplorer /v0.94',
             'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
             'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
             'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
             'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
             'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
             'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.60 Safari/534.24',
             'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
             'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)']

    return headers[i]

def ungzip(data,url):
    try:
        print(url,"正在解压缩...")
        data = gzip.decompress(data)
        print(url,"解压完毕...")
    except:
        print(url,"未经压缩，无需解压...")
    return data

def color(type):
    COLOR = {}
    COLOR['COLOR_GREEN'] = "\033[01;32m"
    COLOR['COLOR_RED'] = "\033[01;31m"
    COLOR['COLOR_YELLOW'] = "\033[01;33m"
    COLOR['COLOR_NONE'] = "\033[m"
    return COLOR[type]

def judgepathsurfix(path):
    if path == "":
        if platform.system() == "Windows":
            path = os.getcwd()+"\\"
        else:
            path = os.getcwd()+"/"
    return path

def judgefile_whether_exist(filepath):
    crush = 1 if os.path.exists(filepath) else print("NOEXIST! START!")
    print(filepath)
    if crush:
        choice = str(input(COLOR_RED+"DO YOU WANT TO DELETE FILE?[y/N]"+COLOR_NONE+":\n"))
        if choice.lower() == 'y' or choice.lower() == 'yes':
            os.remove(filepath)
