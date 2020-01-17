# python day 11
# author zach.wang

import socket,time
sk = socket.socket()
print("this is zach server:\n")
ip=("127.0.0.1",8888)
sk.bind(ip)
# 排队个数
sk.listen(10)
conn, addr = sk.accept()
conn.send("welcome to zach server".encode())
count = 0
run = True
while run:
    print("waiting...")
    recv_data = conn.recv(1024)
    data = recv_data.decode()
    print(data)
    recvtime = time.strftime("%Y-%m-%d %X")
    count += 1
    title ="[" + recvtime + "]" + "\t" + str(count) + " messages\n"
    conn.send(title.encode())
    run = False if data.split('\n')[-1] == "bye" else True


conn.close()