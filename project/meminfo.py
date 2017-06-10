#! /usr/bin/env python
#Filename:meminfo.py
from __future__ import print_function
from collections import OrderedDict
def meminfo():
    '''return the info of /proc/meminfo
    as a dictionary
    '''
    meminfo = OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

if __name__ == '__main__':
    meminfo = meminfo()
    print("Total memory:{0}".format(meminfo['MemTotal']))
    print("Free memory:{0}".format(meminfo['MemFree']))
