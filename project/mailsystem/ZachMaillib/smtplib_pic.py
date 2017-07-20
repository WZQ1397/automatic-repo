# python day 22
# author zach.wang
# -*- coding:utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

sender = '641651925@qq.com'
receiver = 'wzq1397@live.cn'
subject = 'python email test'
smtpserver = 'smtp.qq.com'
port = '465'
username = '641651925'
password = 'vatggmloaqchbbhi'

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'

msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>good!','html','utf-8')
msgRoot.attach(msgText)

fp = open('E:\\python\\redis.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

smtp = smtplib.SMTP_SSL(smtpserver,port)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()