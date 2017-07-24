# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = '641651925@qq.com'
receiver = 'wzq1397@live.cn'
subject = 'python email test'
smtpserver = 'smtp.qq.com'
port = '465'
username = '641651925'
password = 'vatggmloaqchbbhi'
msg['Subject'] = 'test message'


msg = MIMEMultipart('related')

#构造附件
att = MIMEText(open('E:\\python\\redis.png', 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="redis bit"'
msg.attach(att)

smtp = smtplib.SMTP_SSL(smtpserver,port)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()
