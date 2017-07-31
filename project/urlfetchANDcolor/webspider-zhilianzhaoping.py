from urllib.parse import *
from urllib import request
from bs4 import BeautifulSoup
import string
import random
import pandas as pd
import os


headers=["Mozilla/5.0 (Windows NT 6.1; Win64; rv:27.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
         "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:27.0) Gecko/20100101 Firfox/27.0"
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
         "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:10.0) Gecko/20100101 Firfox/10.0"
         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/21.0.1180.110 Safari/537.36"
         "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:10.0) Gecko/20100101 Firfox/27.0"
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/34.0.1838.2 Safari/537.36"
         "Mozilla/5.0 (X11; Ubuntu; Linux i686 rv:27.0) Gecko/20100101 Firfox/27.0"
         "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
         ]

def get_content(url,headsers):
    '''''
    @url：需要登录的网址
    @headers：模拟的登陆的终端
    *********************模拟登陆获取网址********************
    '''
    random_header = random.choice(headers)
    req = request.Request(url)
    req.add_header("User-Agent",random_header)
    req.add_header("Get",url)
    req.add_header("Host","sou.zhaopin.com")
    req.add_header("refer","http://sou.zhaopin.com/")
    html = request.urlopen(req)
    contents = html.read()
    #判断输出内容contents是否是字节格式
    if isinstance(contents,bytes):
        #转成字符串格式
        contents=contents.decode('utf-8')
    else:
        print('输出格式正确，可以直接输出')
    ##输出的是字节格式，需要将字节格式解码转成’utf-8‘
    return (contents)

def get_content1(url,headsers):
    '''''
    @url：需要登录的网址
    @headers：模拟的登陆的终端
    *********************模拟登陆获取网址********************
    '''
    random_header = random.choice(headers)
    req = request.Request(url)
    req.add_header("User-Agent",random_header)
    req.add_header("Get",url)
    req.add_header("Host","jobs.zhaopin.com")
    req.add_header("refer","http://sou.zhaopin.com/jobs/searchresult.ashx")
    html = request.urlopen(req)
    contents = html.read()
    #判断输出内容contents是否是字节格式
    if isinstance(contents,bytes):
        #转成字符串格式
        contents=contents.decode('utf-8')
    else:
        print('输出格式正确，可以直接输出')
    ##输出的是字节格式，需要将字节格式解码转成’utf-8‘
    return (contents)

def get_links_from(job, city, page):
    '''''
    @job:工作名称
    @city:网址中城市名称
    @page：表示第几页信息
    @urls：所有列表的超链接，即子页网址

    ****************此网站需要模拟登陆**********************
    返回全部子网页地址
    '''
    urls=[]
    for i in range(page):
        url = "http://sou.zhaopin.com/jobs/searchresult.ashx?jl={}&kw={}&p={}".format(str(city),str(job),i)
        url = quote(url, safe=string.printable)
        info = get_content(url,headers)
        soup = BeautifulSoup(info,"lxml")#设置解析器为“lxml”
        link_urls = soup.select('td.zwmc a')
        for url in link_urls:
            urls.append(url.get('href'))
    return (urls)


#url = "http://s.yingjiesheng.com/result.jsp?keyword=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98&city=217&start=0&period=0&sort=score&jobtype=1"
#get_links_from('南京','数据挖掘', 5)
def get_link_info(url):
    '''''
    @爬取的地址
    *****************获取此网站的有用信息并保存成字典形式****************
    '''
    info = get_content1(url,headers)
    soup = BeautifulSoup(info,"lxml")#设置解析器为“lxml”
    occ_name = soup.select('div.fixed-inner-box h1')[0]
    com_name = soup.select('div.fixed-inner-box h2')[0]
    com_url = soup.select('div.inner-left.fl h2 a')[0]
    welfare = soup.select('div.welfare-tab-box')[0]
    wages = soup.select('div.terminalpage-left strong')[0]
    exper = soup.select('div.terminalpage-left strong')[4]
    area = soup.select('div.terminalpage-left strong')[1]
    Edu = soup.select('div.terminalpage-left strong')[5]
    cate = soup.select('div.terminalpage-left strong')[7]
    com_nature = soup.select('ul.terminal-ul.clearfix li strong')[9]
    com_address = soup.select('ul.terminal-ul.clearfix li strong')[11]
    '''
    com_scale = soup.select('ul.terminal-ul.clearfix li strong')[8]
    nature = soup.select('div.terminalpage-left strong')[3]
    num = soup.select('div.terminalpage-left strong')[6]
    date = soup.select('div.terminalpage-left strong')[2]
    com_cate = soup.select('ul.terminal-ul.clearfix li strong')[10]
    '''
    data = {
        "网址":url,
        "工作名称":occ_name.text.strip(),
        "公司名称":com_name.text,
        "公司网址":com_url.get('href'),
        "福利":welfare.text.strip(),
        "月工资":wages.text.strip(),
        #"发布日期":date.text.strip(),
        "经验":exper.text.strip(),
        #"人数":num.text.strip(),
        "工作地点":area.text.strip(),
        #"工作性质":nature.text.strip(),
        "最低学历":Edu.text.strip(),
        "职位类别":cate.text.strip(),
        #"公司规模":com_scale.text.strip(),
        "公司性质":com_nature.text.strip(),
        #"公司行业":com_cate.text.strip(),
        "公司地址":com_address.text.strip()
    }
    return (data)
#url = "http://jobs.zhaopin.com/145913042250065.htm"
#get_link_info(url)

def get_links_all_info(job, city, page):
    '''''
    @job:工作名称
    @city:网址中城市名称
    @page：表示前几页信息
    将全部信息保存成矩阵形式，去除无用信息，并在当前目录下生成文件夹并此文件夹下把信息分类保存成.csv格式
    '''
    urls = get_links_from(job, city, page)
    df = pd.DataFrame({

        "网址":[],
        "工作名称":[],
        "公司名称":[],
        "公司网址":[],
        "福利":[],
        "月工资":[],
        #"发布日期":[],
        "经验":[],
        #"人数":[],
        "工作地点":[],
        #"工作性质":[],
        "最低学历":[],
        "职位类别":[],
        #"公司规模":[],
        "公司性质":[],
        #"公司行业":[],
        "公司地址":[],
    })
    links = []
    for url in urls:
        if "xiaoyuan" in url:
            links.append(url)
            columns = ['校园招聘地址']
            labeled_df = pd.DataFrame(columns=columns, data=links)
            #labeled_df.to_csv('{}\{}校园招聘{}地址.csv'.format(str(city)+str(job),str(city),str(job)))
        else:
            data = get_link_info(url)
            #print (data)
            df = df.append(data,ignore_index=True)
    return df

def remove_useless_info(df):
    '''''
    @Dataframe筛选数据 http://jingyan.baidu.com/article/0eb457e508b6d303f0a90572.html
    @df: 以矩阵形式存储爬取到的数据
    定义一个列表，存储指定列类型，
    删除需要删除的类型，
    利用isin()函数保留剩下的数据
    '''
    df = df[ (df.经验 !='5-10年') & (df.经验 !='10年以上') & (df.最低学历 !='博士')]
    return df

def save_info(job, city, page,df):
    '''''
    **************公司性质问题**************
    '''
    #print (list(df.公司性质))
    '''''
    @df_pri = df[df.公司性质.isin('民营')]
    @error:
    only list-like objects are allowed to be passed to isin(), you passed a [str]
    '''
    df_pri = df[df.公司性质.isin(['民营'])]
    df_com = df[df.公司性质.isin(['上市公司'])]
    df_sta = df[df.公司性质.isin(['国企'])]
    df_fore = df[df.公司性质.isin(['外商独资'])]
    df_joint = df[df.公司性质.isin(['合资'])]
    df_Gov = df[df.公司性质.isin(['事业单位'])]
    df_stock = df[df.公司性质.isin(['股份制企业'])]

    #    path = "E:\研究生阶段学习\编程语言\python\python爬虫\python源\招聘资料\智联招聘\job"
    #获取当前路径
    path = os.getcwd()
    #自动生成文件夹并命名
    os.mkdir(r'{}'.format(str(city)+str(job)))
    df_pri.to_csv('{}\{}{}——民营.csv'.format(str(city)+str(job),str(city),str(job)))
    df_com.to_csv('{}\{}{}——上市公司.csv'.format(str(city)+str(job),str(city),str(job)))
    df_sta.to_csv('{}\{}{}——国企.csv'.format(str(city)+str(job),str(city),str(job)))
    df_fore.to_csv('{}\{}{}——外商独资.csv'.format(str(city)+str(job),str(city),str(job)))
    df_joint.to_csv('{}\{}{}——合资.csv'.format(str(city)+str(job),str(city),str(job)))
    df_Gov.to_csv('{}\{}{}——事业单位.csv'.format(str(city)+str(job),str(city),str(job)))
    df_stock.to_csv('{}\{}{}——股份制企业.csv'.format(str(city)+str(job),str(city),str(job)))

def get_recuite_info(job, city, page):
    '''''
    获取招聘信息
    '''
    df = get_links_all_info(job, city, page)
    df_cleaned = remove_useless_info(df)
    save_info(job, city, page, df_cleaned)
'''''
*********************获取招聘信息***************************
'''
get_recuite_info('运维', '上海', 5)


