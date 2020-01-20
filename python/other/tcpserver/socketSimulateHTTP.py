import socket
from urllib.parse import urlparse


class ParserUrl(object):
    '''
    对url进行解析，并返回域名和路径
    '''

    def __init__(self, url):
        self.url = url

    def get_host_path(self):
        parser_url = urlparse(self.url)
        host, path = parser_url.netloc, parser_url.path
        if path:
            return host, path
        else:
            return host, '/'


class SocketHttp(object):
    '''
    需要一个ParserUrl对象，获取host和path
    建立连接返回http response字符串
    http数据传递的时是以字节为单位的，所以需要编码
    '''

    def __init__(self, parser_url):
        self.host, self.path = parser_url.get_host_path()


    def set_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, 80))
        self.client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(self.path, self.host).encode("utf8"))

    @property
    def data(self):
        self.set_socket()
        data = b""
        while True:
            d = self.client.recv(1024)
            if d:
                data += d
            else:
                break
        self.close_socket()
        return data.decode("utf8")

    @property
    def html_content(self):
        html_data = self.data
        return html_data.split("\r\n\r\n")[1]

    def close_socket(self):
        self.client.close()


if __name__ == "__main__":
    url = ParserUrl('https://www.baidu.com/')
    socket_http = SocketHttp(url)
    print(socket_http.html_content)