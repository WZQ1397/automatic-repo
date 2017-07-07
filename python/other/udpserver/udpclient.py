import socket

server_address = ('10.112.5.173', 10000)
message = 'start!'
while True and message:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Send data
        print('sending {!r}'.format(message))
        sent = sock.sendto(str(message).encode('utf-8'), server_address)
        #FIXME 或者 bytes('xxx',encoding='utf-8')

        # Receive response
        print('waiting to receive')
        data, server = sock.recvfrom(4096)
        print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()
        message = input()