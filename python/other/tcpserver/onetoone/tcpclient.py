# python day 11
# author zach.wang
import socket,time
sk = socket.socket()
ip=("127.0.0.1",8888)
sk.connect(ip)
skreply = sk.recv(1000)
print(skreply.decode())
count = 0
run = True
while run:
    msg = input()
    count += 1
    recvtime = time.strftime("%Y-%m-%d %X")
    title ="[" + recvtime + "]" + "\t" + str(count) + " messages\n" + msg
    sk.sendall(title.encode())
    skreply = sk.recv(1024)
    print(skreply.decode())
    run = False if msg == "bye" else True

sk.close()