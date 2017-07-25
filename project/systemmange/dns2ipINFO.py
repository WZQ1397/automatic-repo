import socket
HOSTS = [
    'www.python.org',
    'www.1080pdy.com'
]

for host in HOSTS:
    try:
    #TODO 解析hostname
        print('{} : {}'.format(host, socket.gethostbyname(host)))
    #TODO 详细解析
        name, aliases, addresses = socket.gethostbyname_ex(host)
    #TODO IP-->域名
        #hostname, aliases, addresses = socket.gethostbyaddr('10.9.0.10')
        print('  Hostname:', name)
        print('  Aliases :', aliases)
        print(' Addresses:', addresses)
    #TODO 转换为FQDN
        print('{:>10} : {}'.format(host, socket.getfqdn(host)))

    except socket.error as msg:
        print('{} : {}'.format(host, msg))


def get_constants(prefix):
    """Create a dictionary mapping socket module
    constants to their names.
    """
    return {
        getattr(socket, n): n
        for n in dir(socket)
        if n.startswith(prefix)
    }


families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

responses = socket.getaddrinfo(
    host='www.python.org',
    port='http',
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    proto=socket.IPPROTO_TCP,
    flags=socket.AI_CANONNAME,
)

for response in responses:
    # Unpack the response tuple
    family, socktype, proto, canonname, sockaddr = response

    print('Family        :', families[family])
    print('Type          :', types[socktype])
    print('Protocol      :', protocols[proto])
    print('Canonical name:', canonname)
    print('Socket address:', sockaddr)
    print()