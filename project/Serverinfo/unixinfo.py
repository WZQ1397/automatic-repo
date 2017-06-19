#from Serverinfo import basicinfo
import socket,time,subprocess,re
def dynamicinfo():
    info = {}
    info['sysver'] = subprocess.getstatusoutput("head -1 /etc/issue | awk '{ for(;i++<NF;) \
    if ($i==\"\\n\" ||  $i==\"\l\") continue ; else print $i }'")
    #info['hostname'] = subprocess.getstatusoutput("hostname")
    #currentproccessnum = "(ps -ef | wc -l) -1"
    info['loadavg'] = subprocess.getstatusoutput("more /proc/loadavg  | cut -d \" \" -f 1-3")
    info['uptime'] = subprocess.getstatusoutput("uptime | cut -d \",\" -f 1")
    info['diskusage'] = subprocess.getstatusoutput("df -h | grep ^/dev/* | awk '{print $4,$5}'")
    info['ipv4'] = subprocess.getstatusoutput("ip -4 a | grep inet | grep -v \"127.0.0.1\" | cut -d \" \" -f 6,11 | head -1")


    return info

def conn(mesg):
    sk = socket.socket()
    ip=("127.0.0.1",8888)
    sk.connect(ip)
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = mesg
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    if msg == "bye":
        sk.close()

def main():
    #basicinfo.sendbasicinfo()
    #from Serverinfo.unixtool import diskinfo,meminfo,main
    from Serverinfo.unixtool import main
    conn(main.main())
    time.sleep(1)
    conn(dynamicinfo())

main()
