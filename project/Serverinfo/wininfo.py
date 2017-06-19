# python day 24
# author zach.wang
# -*- coding:utf-8 -*-

import subprocess,socket,time
from Serverinfo import basicinfo

def win_agent_serv_info():
    wininfo = {}
    wininfo['Cpu'] = subprocess.getstatusoutput('wmic cpu list brief')

    wininfo['PsyMem'] = subprocess.getstatusoutput('wmic memphysical list brief')

    wininfo['VirtMem'] =subprocess.getstatusoutput('wmic pagefile list brief')

    wininfo['disk'] = subprocess.getstatusoutput('wmic volume get name,freespace')

    wininfo['IPv4'] = subprocess.getstatusoutput('ipconfig | findstr IPv4')

    return wininfo

def sendadvinfo():
    sk = socket.socket()
    ip=("127.0.0.1",8888)
    sk.connect(ip)
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = win_agent_serv_info()
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    if msg == "bye":
        sk.close()

basicinfo.sendbasicinfo()
time.sleep(1)
sendadvinfo()