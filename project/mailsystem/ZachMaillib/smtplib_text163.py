# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText

to_list = ['wzq1397@live.cn']
smtpserver = 'smtp.163.com'
port = 25
username = '18916295546@163.com'
password = '52xyc1314'


def send(to_list, sub, content):
    '''
    :param to_list: 收件人邮箱
    :param sub: 邮件标题
    :param content: 内容
    '''
    me = "manager" + "<" + username + ">"
    # _subtype 可以设为html,默认是plain
    msg = MIMEText(content, _subtype='html')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(smtpserver,port)
        server.login(username, password)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    send(to_list, "这个是一个邮件", "<h1>Hello, It's test email.</h1>")