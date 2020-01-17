#-*- coding:utf-8 -*-
# python day 27
# author zach.wang
import socket
check = 1
sk = socket.socket()
ip=("127.0.0.1",80)
sk.connect(ip)
def conn():
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = input()
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    return 0 if msg.lower() in ["bye","exit"] else 1

while True and check:
    check = conn()
sk.close()
print("disconnected")