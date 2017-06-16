# python day 25
# author zach.wang
# -*- coding:utf-8 -*-
import time

def _read_cpu_usage():
    """Read the current system cpu usage from /proc/stat"""
    statfile = "/proc/stat"
    cpulist = []
    try:
        f = open(statfile, 'r')
        lines = f.readlines()
    except:
        return []
    for line in lines:
        tmplist = line.split()
        if len(tmplist) < 5:
            continue
        if tmplist[0].startswith('cpu'):
            cpulist.append(tmplist)
    f.close()
    return cpulist

def get_cpu_usage():
    cpuusage = {}
    cpustart = {}
    cpuend = {}
    linestart = _read_cpu_usage()
    if not linestart:
        return 0
    for cpustr in linestart:
        usni=int(cpustr[1])+int(cpustr[2])+int(cpustr[3])+int(cpustr[5])+int(cpustr[6])+int(cpustr[7])+int(cpustr[4])
        usn=int(cpustr[1])+int(cpustr[2])+int(cpustr[3])
        cpustart[cpustr[0]] = str(usni)+":"+str(usn)
    sleep = 2
    time.sleep(sleep)
    lineend = _read_cpu_usage()
    if not lineend:
        return 0
    for cpustr in lineend:
        usni=int(cpustr[1])+int(cpustr[2])+int(cpustr[3])+int(cpustr[5])+int(cpustr[6])+int(cpustr[7])+int(cpustr[4])
        usn=int(cpustr[1])+int(cpustr[2])+int(cpustr[3])
        cpuend[cpustr[0]] = str(usni)+":"+str(usn)
    for line in cpustart:
        start = cpustart[line].split(':')
        usni1,usn1 = float(start[0]),float(start[1])
        end = cpuend[line].split(':')
        usni2,usn2 = float(end[0]),float(end[1])
        cpuper=(usn2-usn1)/(usni2-usni1)
        cpuusage[line] = int(100*cpuper)

    return cpuusage

if __name__ == '__main__':
    print(get_cpu_usage())
else: