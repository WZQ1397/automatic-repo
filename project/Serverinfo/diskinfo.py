# -*-coding:utf-8-*-
#
import re
def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (10**15, 'PB'),
        (10**12, 'TB'),
        (10**9, 'GB'),
        (10**6, 'MB'),
        (10**3, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f%s' % (precision, round(float(bytesize) / factor), suffix)
def dev_phy_size():
  with open('/proc/partitions','r') as dp:
    res = ''
    for disk in dp.readlines():
      if re.search(r'[s,h,v]d[a-z]\n',disk):
        blknum = disk.strip().split(' ')[-2]
        dev = disk.strip().split(' ')[-1]
        size = int(blknum)*1000
        consist = dev+':'+humanize_bytes(size).strip()
        res += consist + '\n'
    return res[:-1]
print(dev_phy_size())
