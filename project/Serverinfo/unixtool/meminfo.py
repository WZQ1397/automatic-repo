# python day 28
# author zach.wang
#! /usr/bin/env python
#Filename:meminfo.py
from __future__ import print_function
from collections import OrderedDict
from Serverinfo import humanreadsize
import re

def meminfo():
    '''return the info of /proc/meminfo
    as a dictionary
    '''
    meminfo = OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            size = list(re.compile(r' ').split(line.split(':')[1].strip()))[0]
            size = humanreadsize.humanize_bytes(float(size)*1000)
            meminfo[line.split(':')[0]] = size
    return meminfo

def memory():
    memdict = {}
    mem = meminfo()
    memdict['MemTotal'] = mem['MemTotal']
    memdict['MemFree'] = mem['MemFree']
    memdict['SwapTotal'] = mem['SwapTotal']
    memdict['SwapFree'] = mem['SwapFree']
    return memdict

if __name__ == '__main__':
    meminfo = meminfo()
    print("Total memory:{0}".format(meminfo['MemTotal']))
    print("Free memory: {0}".format(meminfo['MemFree']))
    print("SwapTotal:   {0}".format(meminfo['SwapTotal']))
    print("SwapFree:    {0}".format(meminfo['SwapFree']))
else:
    memory()