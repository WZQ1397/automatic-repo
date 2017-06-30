#-*- coding:utf-8 -*-
# python day 27
# author zach.wang
import socket
import threading,time

def serverinfo(conn,addr):
    info = ""
    conn.send("welcome to zach server".encode())
    count = 0
    while True:
        try:
            recv_data = conn.recv(10240)
            if not recv_data:
                break
            info = recv_data.decode()
            recvtime = time.strftime("%Y-%m-%d %X")
            count += 1
            title ="[" + recvtime + "]" + "\t" + str(count) + " messages\n"
            conn.send(title.encode())
            print(info)
            if recv_data.decode() == "bye":
                conn.close()
        except ConnectionAbortedError:
            pass
        finally:
            return info


# 客户端列表
clients = []

# 设置IP地址与端口
HOST = '0.0.0.0'
PORT = 80

# 初始化socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定IP地址与端口
s.bind((HOST, PORT))

# 开始监听
s.listen(1)
print("this is zach server:\n")
# 循环等待
while True:
  # 接受客户
  client, addr = s.accept()

  # 启动新的进程与客户通信
  thread = threading.Thread(target=serverinfo,args=(client,addr))

  thread.start()

  # 记录新的客户
  clients.append(client)
