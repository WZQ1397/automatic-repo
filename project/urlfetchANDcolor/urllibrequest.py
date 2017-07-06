from urllib import request
#url = 'https://www.baidu.com'
url = 'http://172.16.6.20:8001/'
COLOR_GREEN = "\033[01;32m"
COLOR_NONE = "\033[m"

response = request.urlopen(url)
print('RESPONSE:', response)
print('URL     :', response.geturl())

headers = response.info()
print('DATE    :', headers['date'])
print('HEADERS :')
print('---------')
#print(headers)

data = response.read().decode('utf-8')
print('LENGTH  :', len(data))
print('DATA    :')
print('---------')
#print(data)

#print(request.urlopen(url).read().decode('utf-8'))

r = request.Request(url)
r.add_header(
    'User-agent',
    'WZQ1397 (https://1080pdy.com/)',
)
response = request.urlopen(r)
print("METHOD:",r.get_method(),"\nGET HEADER:",r.get_header('User-agent'))

#TODO GET ALL BROWSER INFO
print(COLOR_GREEN+'-'*30+COLOR_NONE)
print('Status:', response.status, response.reason)
for k, v in response.getheaders():
    print('%s: %s' % (k, v))

#TODO 配置代理
def proxyurllib():
    print(COLOR_GREEN+'-'*30+COLOR_NONE)
    #TODO proxy
    handler=request.ProxyHandler({'http':'http://10.112.5.173:49908'})
    '''
    proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
    proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
    '''
    opener=request.build_opener(handler)
    request.install_opener(opener)
    #安装opener作为urlopen()使用的全局URL opener，即以后调用urlopen()时都会使用安装的opener对象。response=
    google = request.urlopen('http://www.google.com')
    print(google.read())

    print("代理列表：",request.getproxies())

#proxyurllib()

#FIXME ROBOT.TXT解析
'''https://docs.python.org/3.0/library/urllib.robotparser.html'''