# -*-coding:utf-8-*-
#
import re
from Serverinfo import humanreadsize

def dev_phy_size():
    with open('E:\\automatic-repo\\project\\b.txt','r') as dp:
        res = ''
        for disk in dp.readlines():
            if re.search(r'[s,h,v]d[a-z]\n',disk):
                blknum = disk.strip().split(' ')[-2]
                dev = disk.strip().split(' ')[-1]
                size = int(blknum)*1000
                consist = dev+':'+humanreadsize.humanize_bytes(size).strip()
                res += consist + '\n'
        return res.strip()

def filter(value):
    diskdict = {}
    for x in value.split('\n'):
        diskdict[x.split(':')[0]] = x.split(':')[1]
    #print(diskdict)
'''
if __name__ == '__main__':
    print(dev_phy_size())
else:
    dev_phy_size()
'''
