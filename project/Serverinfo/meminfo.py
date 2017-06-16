#! /usr/bin/env python
#Filename:meminfo.py
from __future__ import print_function
from collections import OrderedDict
import re
def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (10**15, 'PB'),
        (10**12, 'TB'),
        (10**9, 'GB'),
        (10**6, 'MB'),
        (10**3, 'KB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f%s' % (precision, float(bytesize) / factor, suffix)

def meminfo():
    '''return the info of /proc/meminfo
    as a dictionary
    '''
    meminfo = OrderedDict()
    with open('/proc/meminfo') as f:
        for line in f:
            size = list(re.compile(r' ').split(line.split(':')[1].strip()))[0]
            size = humanize_bytes(float(size)*1000)
            meminfo[line.split(':')[0]] = size
    return meminfo



if __name__ == '__main__':
    meminfo = meminfo()
    print("Total memory:{0}".format(meminfo['MemTotal']))
    print("Free memory: {0}".format(meminfo['MemFree']))
    print("SwapTotal:   {0}".format(meminfo['SwapTotal']))
    print("SwapFree:    {0}".format(meminfo['SwapFree']))