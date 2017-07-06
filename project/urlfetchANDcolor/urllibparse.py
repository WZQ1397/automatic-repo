from urllib.parse import urlsplit,urljoin,urlencode,parse_qs,parse_qsl,quote_plus
COLOR_GREEN = "\033[01;32m"
COLOR_RED = "\033[01;31m"
COLOR_YELLOW = "\033[01;33m"
COLOR_NONE = "\033[m"

###TODO MODULE1
url = ['http://www.1080pdy.com/plugin.php?id=zb7com_sign:sign&signop=sign&formhash=538f267b',
       'ssh://wzq1397@1080pdy.com:2022']

for parsed in url:
    parsed = urlsplit(parsed)
    print('scheme  :', parsed.scheme)
    print('netloc  :', parsed.netloc)
    print('path    :', parsed.path)
    print('query   :', parsed.query)
    print('fragment:', parsed.fragment)
    print('username:', parsed.username)
    print('password:', parsed.password)
    print('hostname:', parsed.hostname)
    print('port    :', parsed.port)
    print("="*30)

###TODO MODULE2
print(COLOR_YELLOW+"Urljoin".center(30))
step1=urljoin('http://www.1080pdy.com/search/file.html',
              '../enginesphinx.php')
print(step1)

query_args = {
    'q': ['1080pdy','xyc'],
    'ie': 'utf8',
    'u': 'wzq1397',
    'bs': 'movies'
}
urlarg="?"+urlencode(query_args)
#TODO 不加编码
#urlarg="?"+urlencode(query_args, doseq=True)

step2 = urljoin(step1,urlarg)
print(step2)

###TODO MODULE3
print("*"*30+COLOR_NONE)
print("获取请求列表（qsl是元祖）")
qs = urlsplit(step2).query
print('query   :', parse_qs(qs))
print('query   :', parse_qsl(qs))
print('quote   :', quote_plus(step2))
#TODO 相反
from urllib.parse import unquote,unquote_plus
print("*"*30+)