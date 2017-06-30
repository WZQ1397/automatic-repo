#-*- coding:utf-8 -*-
# python day 27
# author zach.wang
import socket
check = 1
def conn():
    sk = socket.socket()
    ip=("127.0.0.1",80)
    sk.connect(ip)
    skreply = sk.recv(1000)
    print(skreply.decode())
    count = 0
    msg = input()
    count += 1
    sk.sendall(str(msg).encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    print(str(msg))
    if str(msg).lower == "bye" or str(msg).lower == "exit":
        return 0
    else:
        return 1

while True and check:
    check = conn()
