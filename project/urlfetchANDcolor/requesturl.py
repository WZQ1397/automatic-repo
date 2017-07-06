import requests,yaml
web = 'http://ava.qq.com/act/a20090522honor/index.htm'
url = requests.get(web)
print(url.url)
#print("Data:\n",url.text) #bytes --> url.content
print("Method:\n",url.request,"\n重定向:",url.is_redirect)
print("\033[01;32mHTTP Header:\033[m".center(50,'-'))
for k,v in url.headers.items():
    print(k,":",v)
print("页面状态:",url.status_code == requests.codes.ok)


#json 专用
url = requests.get('http://172.16.6.20:8001/')
print(yaml.dump(url.json()))
'''
#TODO 提交数据
chhead = ['Cache-Control', 'max-age=30']
cookies = dict(cookies_are='working')
url = requests.post(web,data=chhea,cookies=cookies)
#url = requests.put(web,data=chhea,cookies=cookies)
# FIXME 如果URL可以在客户端确定，那么就使用PUT，如果是在服务端确定，那么就使用POST
print(url.text)

#TODO 定制请求头,模拟浏览器抓取
url = 'http://m.ctrip.com'
headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
r = requests.post(url, headers=headers)

#提交文件
url = 'http://m.ctrip.com'
files = {'file': open('report.xls', 'rb')}
r = requests.post(url, files=files)
'''

#TODO 删除资源
print("\033[01;32mAFTER MODIFY Header:\033[m".center(50,'-'))
url = requests.delete(web,data='Last-Modified')
for k,v in url.headers.items():
    print(k,":",v)

url = requests.head(web)
print(url.headers)

#TODO 设置代理
proxies = {'http':'http://10.112.5.173:49908'}
url = requests.get('http://www.google.com', proxies=proxies)
print(url.status_code)