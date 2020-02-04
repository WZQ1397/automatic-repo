import socket
"""
协程实现socket高并发的客户端
"""
 
 
client = socket.socket()
 
client.connect(("localhost", 6666))
 
 
while True:
    input_data = input(">>:").strip()
    if not input_data:
        continue
    client.send(input_data.encode())
    data = client.recv(1024).decode()
    print(data)
client.close()
