# python day 23
# author zach.wang
# -*- coding:utf-8 -*-
import platform,re,socket,time
from Serverinfo import humanreadsize,unixinfo


syscheck = str(platform.system()).lower()
def winsysadvinfo(wininfo):
    '''
    info = ""
    infodic = {}
    with open("info.txt","r") as f:
        info = "".join(f.readlines())
    judge = re.compile(r'\n')
    info = judge.split(info)
    judge2 = re.compile(r':')
    for var in info:
        if judge2.split(str(var))[0] == "登录服务器":
            break
        print(judge2.split(str(var)))

    info = judge2.split(info)
    '''
    Maohao = re.compile(r':')
    jinghao = re.compile(r'#')
    Blank = re.compile(r'\s+')
    wininfo = eval(wininfo)

    #TODO CPUINFO
    Cpu = []
    Cpu.append(Maohao.split(re.sub("\s+",":",str(list(re.compile(r'\(R\) ').\
            split(str(list(wininfo['Cpu']))))[0])))[-1])
    Cpu.append(list(re.compile(r'Socket').split(str(list(re.compile(r'\(R\) ').\
                              split(str(list(wininfo['Cpu']))))[-1])))[0])

    #TODO Psycal Memery
    PsyMem = list(Maohao.split(str(re.sub("\s+",":",Maohao.
                 split(re.sub("n",":",str(list(re.compile(r'Physical Memory Array ').\
    split(str(list(wininfo['PsyMem']))))[0])))[-1]))))

    #TODO Virt Memory
    VirtMem = list(Blank.split(str(list(jinghao.split(
        re.sub("\n","#",str(list(
            wininfo['VirtMem'])[-1]))))[-4]).strip()))
    #print(VirtMem[-3],VirtMem[-1])

    #TODO DISKINFO
    disk = list(re.compile(r'\\n\\n').split(str(list(wininfo['disk']))))[1:]
    Diskdetail = []
    for x in range(0,len(disk)-1):
        Diskdetail.append(list(Blank.split(str(disk[x]).strip())))
        #print("{} {:.2f}GB".format(Diskdetail[1],int(str(Diskdetail[0]))/(1024**3)))

    #TODO IPV4 ADDR
    IPv4 = list(Maohao.split(str(list(wininfo['IPv4'])[-1])))[-1]

    dic = {}
    dic['Cpu'] = Cpu
    dic['PsyMem'] = PsyMem
    dic['VirtMem'] = VirtMem
    dic['Diskdetail'] = Diskdetail
    dic['IPv4'] = IPv4

    return dic

def beautiful_print(info):
    if syscheck == "windows":
        wininfo = winsysadvinfo(info)
        diskinfo = {}
        #print(re.sub(",","\n",str()))
        for disk in wininfo['Diskdetail']:
            size = humanreadsize.humanize_bytes(int(disk[0]))
            '''
            if size < 1:
                size = str(int(disk[0])//(1024**2))+"MB"
            else:
                size = str(size)+"GB"
            '''
            diskinfo[re.sub("\\\\","",disk[1])] = size
        diskstr = re.sub("\'|\{|\}","",str(diskinfo))

        virt1 = "文件地址:{}".format(str(wininfo['VirtMem'][-2:][0]))
        virt2 = "文件大小:{}MB".format(str(wininfo['VirtMem'][-2:][-1]))

        cpuinfo0 = str(eval(str(wininfo['Cpu']))[0])+"  "
        cpuinfo1 = str(eval(re.sub("\s+"," ",str(wininfo['Cpu'])))[1])

        return '''
        CPU型号:              {}
        最大支持物理内存大小: {}
        当前网络内存大小:     {}
        虚拟内存大小:         {}
        主IP地址:             {}
        磁盘信息:{}
        '''.format(cpuinfo0+cpuinfo1,str(int(wininfo['PsyMem'][0])/1048576)+"GB",str(int(wininfo['PsyMem'][1]))+"GB",
                   virt1+"\n"+"\t"*7+"  "+virt2,wininfo['IPv4'],"\t"*3+re.sub(",","\n\t\t\t\t\t\t   ",diskstr))
    else:
        pass


def linux():
    unixinfo.main()

def serverinfo():
    info = ""
    sk = socket.socket()
    #print("this is zach server:\n")
    ip=("127.0.0.1",8888)
    sk.bind(ip)
    sk.listen(10)
    conn, addr = sk.accept()
    conn.send("welcome to zach server".encode())
    count = 0
    try:
        recv_data = conn.recv(10240)
        info = recv_data.decode()
        recvtime = time.strftime("%Y-%m-%d %X")
        count += 1
        title ="[" + recvtime + "]" + "\t" + str(count) + " messages\n"
        conn.send(title.encode())
        #print(info)
        if recv_data.decode() == "bye":
            conn.close()
    except ConnectionAbortedError:
        pass
    finally:
        return info

if syscheck != "windows":
    print(serverinfo())
    info = serverinfo()
    print(beautiful_print(info))
else:
    linux()

