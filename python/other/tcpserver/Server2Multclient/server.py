#-*- coding:utf-8 -*-
# python day 27
# author zach.wang
import socket
import threading,time
import signal,sys
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

def sigintHandler():
  sys.exit(1)


if __name__ == '__main__':
  # 信号捕捉程序必须在循环之前设置
  signal.signal(signal.SIGINT, sigintHandler)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
  signal.signal(signal.SIGTERM, sigintHandler)  # 请求中止进程，kill命令缺省发送

  # 循环等待
  while True:
    # 接受客户
    client, addr = s.accept()
    # 启动新的进程与客户通信
    thread = threading.Thread(target=serverinfo,args=(client,addr))
    thread.start()
    # 记录新的客户
    clients.append(client)