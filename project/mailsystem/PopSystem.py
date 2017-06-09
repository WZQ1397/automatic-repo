# python day 23
# author zach.wang
# -*- coding:utf-8 -*-
from email.parser import Parser
# email.parser 解析电子邮件
# 返回这个对象的email.message.Message实例
from email.header import decode_header
from email.utils import parseaddr
import poplib,sys

#options
username = '18916295546@163.com'
receiver = "zach.wang" + "<" + username + ">"
pop3server = 'pop.163.com'
port = '995'
password = '52xyc1314'
pop3 = poplib.POP3_SSL(pop3server,port)

def pop3_login():
    #pop3.set_debuglevel(1)
    global mails
    print(pop3.getwelcome().decode("utf-8"))
    pop3.user(username)
    pop3.pass_(password)
    #print(pop3.stat())
    resp, mails, octets = pop3.list()
    #print("list",pop3.list())
    # 返回的列表类似[b'1 82923', b'2 2184', ...]
    print(mails)

# TODO 模版区域
# 邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode
def decode_str(s):
    value, charset = decode_header(s)[0]
    # decode_header()返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素。上面的代码我们偷了个懒，只取了第一个元素。
    if charset:
        value = value.decode(charset)
    return value


# 文本邮件的内容也是str，还需要检测编码，否则，非UTF-8编码的邮件都无法正常显示
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# 解析邮件与构造邮件的步骤正好相反
def print_info(msg, indent=0):
    if indent ==0:
        for header in ["From", "To", "Subject"]:
            value = msg.get(header, "")
            if value:
                if header == "Subject":
                    value = decode_str(value)
                else:
                    hdr, addr =parseaddr(value)
                    name = decode_str(hdr)
                    value = u"%s <%s>" % (name, addr)
            print("%s%s:%s" % ("  " * indent, header, value))
        if (msg.is_multipart()):
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
                print_info(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type=='text/plain' or content_type=='text/html':
                content = msg.get_payload(decode=True)
                charset = guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content + '...'))
            else:
                print('%sAttachment: %s' % ('  ' * indent, content_type))


def mail_save_tofile(startnum):
    pop3_login()
    if startnum > len(mails) or startnum < 0:
        startnum = 1
    else:
        startnum = len(mails)-startnum
    for i in range(startnum,len(mails)+1):
        resp, lines, ocetes = pop3.retr(i)
        msg_content = b"\r\n".join(lines).decode("utf-8")
        # 稍后解析出邮件
        msg = Parser().parsestr(msg_content)
        # email.Parser.parsestr(text, headersonly=False)
        #print(msg)
        filename = decode_str(msg.get("Subject", ""))
        with open(filename+".htm","w+") as f:
            sys.stdout = f
            print_info(msg)

if __name__ != '__main__':
    mail_save_tofile()
else:
    num, flag = 1, 0
    choice = input("do you want to file?[y/N(default:N)]\n")
    if choice.lower() == "y":
        try:
            num = int(input("how many do you want to file?[(default:ALL)]\n"))
        except ValueError:
            sys.stderr.write("This is NOT digit!Use default")
            mail_save_tofile(1)
            flag = 1
        finally:
            if flag != 1:
                mail_save_tofile(num)
    else:
        pop3_login()

pop3.quit()