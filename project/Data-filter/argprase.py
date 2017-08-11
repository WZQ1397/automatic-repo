# python day 12
# author zach.wang
# -*- coding:utf-8 -*-
import argparse

'''
param :
E:\python>zach1.py -h
usage: zach1.py [-h] [--dir DIR] [-n NUM] name

positional arguments:
  name               create name for dir

optional arguments:
  -h, --help         show this help message and exit
  --dir DIR          which loc to create
  -n NUM, --num NUM  how many do you want to create
'''
#TODO E:\python>zach1.py --dir ok -n 5 zach
#TODO you want to create 5 zach dir in ok
#XXX AAAA

helpcmd = argparse.ArgumentParser(description='create some dir coustomly.')
helpcmd.add_argument("name",type=str,help="create name for dir",default="zach")
helpcmd.add_argument("--dir",type=str,help="which loc to create",default="E:\\python")
helpcmd.add_argument("-n","--num",type=int,help="how many do you want to create",default=1)
args = helpcmd.parse_args()
print('you want to create %d %s dir in %s' %(args.num,args.name,args.dir))


