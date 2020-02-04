import gevent
from gevent import monkey
monkey.patch_all()
import socket
"""
协程实现socket的高并发服务器
"""
 
 
def handle_data(conn):
    try:
        while True:
            data = conn.recv(1024)
            print("==> [{}]".format(data.decode('UTF-8')))
            if not data:
                conn.shutdown(socket.SHUT_WR)
            conn.send(data.upper())
    except exception as ex:
        print(ex)
    finally:
        conn.close()
 
def my_server(port):
    server = socket.socket()
    #绑定地址和端口
    server.bind(("0.0.0.0", port))
    #开始监听
    server.listen(500)
    while True:
        #阻塞等待连接
        conn, addr = server.accept()
        #来数据了
        gevent.spawn(handle_data, conn)
 
 
if __name__ == '__main__':
    my_server(6666)
