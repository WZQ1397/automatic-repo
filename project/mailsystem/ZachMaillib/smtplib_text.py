# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText

#options
sender = '641651925@qq.com'
receiver = '18916295546@163.com'
subject = 'python email'
smtpserver = 'smtp.qq.com'
port = '465'
username = '641651925'
password = 'vatggmloaqchbbhi'

msg = MIMEText('hello, send by Python...','plain','utf-8')
msg['Subject'] = subject

smtp = smtplib.SMTP_SSL(smtpserver,port)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()