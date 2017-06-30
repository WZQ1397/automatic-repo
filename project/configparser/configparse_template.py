# author zach.wang
# -*- coding:utf-8 -*-
from configparser import ConfigParser, ExtendedInterpolation

CONFFILE = 'conf.ini'
#TODO 解析块变量 ${default_pass:username}，如果启用此格式失效 %(xxx)s
#parser = ConfigParser(allow_no_value=True,interpolation=ExtendedInterpolation())
parser = ConfigParser(allow_no_value=True)
parser.read(CONFFILE)

print("first: {}\n".format(parser.get('bug_tracker', 'url')))

for name in parser.sections():
    print("section:" ,name)
    print('  Options:', parser.options(name))
    for name, value in parser.items(name):
        print('  {} = {}'.format(name, value))

parser.add_section("zach")
parser.set("zach","xyc","yes")
print("\n-----\nweather has zach section?\n",parser.has_section("zach"))
print("\n-----\nweather has zach opt?\n",parser.has_option("zach","xyc"))
parser.set('wiki','server',"172.16.10.120")
parser.write(open(CONFFILE,mode='w'))

print("Alter: {}\n".format(parser.get('wiki', 'url')))